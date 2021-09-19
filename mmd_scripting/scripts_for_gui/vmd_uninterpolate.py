import math
from typing import List, Tuple, Set, Sequence
import random

import mmd_scripting.core.nuthouse01_core as core
import mmd_scripting.core.nuthouse01_vmd_parser as vmdlib
import mmd_scripting.core.nuthouse01_vmd_struct as vmdstruct
import mmd_scripting.core.nuthouse01_vmd_utils as vmdutil
from mmd_scripting.vectorpaths_chrisarridge import vectorpaths


_SCRIPT_VERSION = "Script version:  Nuthouse01 - v1.07.05 - 9/7/2021"
# This code is free to use and re-distribute, but I cannot be held responsible for damages that it may or may not cause.
#####################
# https://github.com/chrisarridge/vectorpaths

DEBUG = True
DEBUG_PLOTS = True

if DEBUG:
	import logging
	# this prints a bunch of useful stuff in the bezier regression, and a bunch of useless stuff from matplotlib
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

if DEBUG_PLOTS:
	import matplotlib.pyplot as plt

helptext = '''=================================================
vmd_uninterpolate:
Modify a VMD and remove excess keyframes caused by deliberate over-keying.
This will make the VMD much smaller (filesize) and make it easier to load or tweak for different models.
WARNING: THIS TAKES AN EXTREMELY LONG TIME TO RUN!

Output: dunno
'''

'''
data: how for bone センター in Marionette, how many frames are kept based on position for varying bezier error targets
errors 0.5 - 3.0
total=6212

0.5, keep%=59%
0.6, keep%=54%
0.7, keep%=50%
0.79, keep%=46%
0.89, keep%=42%
0.99, keep%=38%
1.09, keep%=36%
1.2, keep%=34%
1.3, keep%=33%
1.4, keep%=32%
1.5, keep%=30%
1.6, keep%=30%
1.7, keep%=29%
1.8, keep%=28%
1.9, keep%=27%
2.0, keep%=26%
2.1, keep%=25%
2.2, keep%=25%
2.3, keep%=24%
2.4, keep%=23%
2.5, keep%=22%
2.6, keep%=22%
2.7, keep%=21%
2.8, keep%=21%
2.9, keep%=21%
'''

SIMPLIFY_BONE_POSITION = False
SIMPLIFY_BONE_ROTATION = True

MORPH_ERROR_THRESHOLD = 0.00001

BEZIER_ERROR_THRESHOLD_BONE_POSITION_RMS = 1.2
BEZIER_ERROR_THRESHOLD_BONE_POSITION_MAX = 1.2

BONE_ROTATION_STRAIGHTNESS_VALUE = 0.15

REVERSE_SLERP_TOLERANCE = 0.05

CONTROL_POINT_BOX_THRESHOLD = 2

BONE_ROTATION_MAX_Z_LOOKAHEAD = 500


# TODO: overall cleanup, once everything is acceptably working. variable names, comments, function names, etc.

# TODO: change morph-simplify to use a structure more similar to the bone-simplify structure? i.e. store frame
#  indices in a set and then get the frames back at the very end. it would be less efficient but its just for
#  more consistency between sections.

# TODO: optimize the position section of bone-simplify, add another loop layer so i don't need to keep re-finding z.

# TODO: do something to ensure that bezier control points are guaranteed within the box...
#  clamp it afterward? somehow change the regression algorithm to restrict them at each step?
#  ALSO want to compute exactly how often the points are outside the box.
#  **BEST**: if control points are outside the box, then it doesn't represent a curve that's possible in MMD! discard it!

# TODO: modify the bezier regression to return the error values? i think it would just be for logging, not sure if its
#  worth changing the structure.
#  it would be useful for, "keep walking backward until you find a curve that's good, and the NEXT curve is worse"...?
#  except that no, if region M can be well fit then any subset of the region can be fit as well or better...

# TODO: even more testing to figure out what good values are for bezier error targets

# TODO: how the fuck can i effectively visualize quaternions? i need to see them plotted on a globe or something
#  so i can have confidence that my "how straight should be considered a straight line" threshold is working right

# TODO: re-research how to measure quaternion angle and angular distance (is there a difference?)

# TODO: should quaternion straightness be judged by "AB vs CD" or "AB vs AC" ?

def sign(U):
	# return -1/0/+1 if input is negative/zero/positive
	if U == 0:  return 0
	elif U > 0: return 1
	else:       return -1

def scale_list(L:List[float], R: float) -> List[float]:
	"""
	Take a list of floats, shift/scale it so it starts at 0 and ends at R.
	:param L: list of floats
	:param R: range endpoint
	:return: list of floats, same length
	"""
	assert len(L) >= 2
	# one mult and one shift
	ra = L[-1] - L[0]  # current range of list
	if -1e-6 < ra < 1e-6:
		# if the range is basically 0, then add 0 to the first, add R to the last, and interpolate in between
		offset = [R * s / (len(L)-1) for s in range(len(L))]
		L = [v + o for v,o in zip(L,offset)]
	else:
		# if the range is "real",
		L = [v * R / ra for v in L]  # scale the list to be the desired range
	L = [v - L[0] for v in L]  # shift it so the 0th item equals 0
	return L

def get_difference_quat(quatA: Tuple[float, float, float, float],
						quatB: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
	# get the "difference quaternion" that represents how to get from A to B...
	# or is this how to get from B to A?
	# as long as I'm consistent I don't think it matters?
	deltaquat_AB = core.hamilton_product(core.my_quat_conjugate(quatA), quatB)
	return deltaquat_AB

def get_quat_angular_distance(quatA: Tuple[float, float, float, float],
							  quatB: Tuple[float, float, float, float]) -> float:
	"""
	Calculate the "angular distance" between two quaternions, in radians. Opposite direction = pi = 3.14.
	:param quatA: WXYZ quaternion A
	:param quatB: WXYZ quaternion B
	:return: float radians
	"""
	# https://math.stackexchange.com/questions/90081/quaternion-distance
	# theta = arccos{2 * dot(qA, qB)^2 - 1}
	# unlike previous "get_corner_sharpness_factor", this doesn't discard the W component
	# so i have a bit more confidence in this approach, i think?
	quatA = core.normalize_distance(quatA)
	quatB = core.normalize_distance(quatB)
	
	# TODO: how do i handle if one or both quats are zero-rotation!?
	
	a = core.my_dot(quatA, quatB)
	b = (2 * (a ** 2)) - 1
	c = core.clamp(b, -1.0, 1.0)  # this may not be necessary? better to be safe tho
	d = math.acos(c)
	# d: radians, 0 = same, pi = opposite
	return d / math.pi

def get_corner_sharpness_factor(deltaquat_AB: Tuple[float, float, float, float],
								deltaquat_BC: Tuple[float, float, float, float],) -> float:
	"""
	Calculate a [0.0-1.0] factor indicating how "sharp" the corner is at B.
	By "corner" I mean the directional change when A->B stops and B->C begins.
	If they are going the same angular "direction", then return 1.0. If they
	are going perfectly opposite directions, return 0.0. Otherwise return something
	in between.

	:param deltaquat_AB: "delta quaterinon" WXYZ from frame A to B
	:param deltaquat_BC: "delta quaternion" WXYZ from frame B to C
	:return: float [0.0-1.0]
	"""
	
	# "how sharp a corner is" = the "angular distance" between AtoB delta and BtoC delta
	
	# first, find the deltas between the quaternions
	# deltaquat_AB = core.hamilton_product(core.my_quat_conjugate(quatA), quatB)
	# deltaquat_BC = core.hamilton_product(core.my_quat_conjugate(quatB), quatC)
	# to get sensible results below, ignore the "W" component and only use the XYZ components, treat as 3d vector
	deltavect_AB = deltaquat_AB[1:4]
	deltavect_BC = deltaquat_BC[1:4]
	# second, find the angle between these two deltas
	# use the plain old "find the angle between two vectors" formula
	len1 = core.my_euclidian_distance(deltavect_AB)
	len2 = core.my_euclidian_distance(deltavect_BC)
	if (len1 == 0) and (len2 == 0):
		# zero equals zero, so return 1!
		return 1.0
	t = len1 * len2
	if t == 0:
		# if exactly one vector has a length of 0 (but not both, otherwise it would be caught above) then they are DIFFERENT
		return 0.0
	# technically the clamp shouldn't be necessary but floating point inaccuracy caused it to do math.acos(1.000000002) which crashed lol
	shut_up = core.my_dot(deltavect_AB, deltavect_BC) / t
	shut_up = core.clamp(shut_up, -1.0, 1.0)
	ang_d = math.acos(shut_up)
	# print(math.degrees(ang_d))
	# if ang = 0, perfectly colinear, factor = 1
	# if ang = 180, perfeclty opposite, factor = 0
	factor = 1 - (ang_d / math.pi)
	return factor

def reverse_slerp(q, q0, q1):
	# https://math.stackexchange.com/questions/2346982/slerp-inverse-given-3-quaternions-find-t
	# t = log(q0not * q) / log(q0not * q1)
	# elementwise division, except skip the w component
	q0not = core.my_quat_conjugate(q0)
	a = core.quat_ln(core.hamilton_product(q0not, q))
	b = core.quat_ln(core.hamilton_product(q0not, q1))
	a = a[1:4]
	b = b[1:4]
	if 0 in b:
		# this happens when q0 EXACTLY EQUALS q1... so, if interpolating between Z and Z, you're not moving at all, right?
		# actually, what if something starts at A, goes to B, then returns to A? it's all perfectly linear with
		# start/end exactly the same! but it's definitely 2 segments. so I cant just return a static value.
		# i'll return the angular distance between q and q0 instead, its on a different scale but w/e, it gets
		# normalized to 128 anyways
		x = 100 * get_quat_angular_distance(q0, q)
		return x,x,x
	ret = tuple(aa/bb for aa,bb in zip(a,b))
	return ret
	


def simplify_morphframes(allmorphlist: List[vmdstruct.VmdMorphFrame]) -> List[vmdstruct.VmdMorphFrame]:
	"""
	morphs have only one dimension to worry about, and cannot have interpolation "curves"
	everything is perfectly linear!
	i'm not entirely sure that the facials are over-keyed like the bones are... but it's a good warmup
	turns out that there are a few spots with excessive keys, but it's mostly sparse like i expected

	:param allmorphlist:
	:return:
	"""
	output = []  # this is the list of frames to preserve, the startpoints and endpoints
	
	# verify there is no overlapping frames, just in case
	allmorphlist = vmdutil.assert_no_overlapping_frames(allmorphlist)
	# sort into dict form to process each morph independently
	morphdict = vmdutil.dictify_framelist(allmorphlist)
	
	# analyze each morph one at a time
	for morphname, morphlist in morphdict.items():
		# make a list of the deltas, for simplicity
		thisoutput = []
		# the first frame is always kept. and the last frame is also always kept.
		# if there is only one frame, or two, then don't even bother walking i guess?
		if len(morphlist) <= 2:
			output.extend(morphlist)
			continue
		
		# the first frame is always kept.
		thisoutput.append(morphlist[0])
		i = 0
		while i < (len(morphlist)-1):
			# start walking down this list
			# assume that i is the start point of a potentially over-keyed section
			m_this = morphlist[i]
			m_next = morphlist[i+1]
			delta_rate = (m_next.val - m_this.val) / (m_next.f - m_this.f)
			# now, walk forward from here until i "return" a frame that has a different delta
			z = 0  # to make pycharm shut up
			for z in range(i+1, len(morphlist)):
				# if i reach the end of the morphlist, then "return" the final valid index
				if z == len(morphlist)-1:
					break
				z_this = morphlist[z]
				z_next = morphlist[z + 1]
				delta_z = (z_next.val - z_this.val) / (z_next.f - z_this.f)
				if (delta_rate - MORPH_ERROR_THRESHOLD) < delta_z < (delta_rate + MORPH_ERROR_THRESHOLD):
					# if this is within the tolerance, then this is continuing the slide and should be skipped over
					pass
				else:
					# if this delta is not within some %tolerance of matching, then this is a break!
					break
			# now, z is the index for the end of the sequence
			# it starts at i and ends at z
			# i know that i have found a segment endpoint and i can discard everything in between!
			# no need to preserve 'i', it has already been added
			thisoutput.append(morphlist[z])
			# now skip ahead and start walking from z
			i = z
		if DEBUG:
			# when i am done with this morph, how many have i lost?
			tossed = len(morphlist) - len(thisoutput)
			if tossed:
				print(morphname)
				print("tossed %d frames" % tossed)
				for i in range(len(morphlist)):
					m = morphlist[i]
					if i == len(morphlist)-1:
						delta = 999
					else:
						m2 = morphlist[i+1]
						delta = (m2.val - m.val) / (m2.f - m.f)
					print("%s n:%s f:%d v:%f d:%f" % ("*" if m in thisoutput else " ", morphname, m.f, m.val, delta))
		
		output.extend(thisoutput)
	# FIN
	print("TOTAL: tossed %d frames" % (len(allmorphlist) - len(output)))
	
	return output

def _simplify_boneframes_position(bonename: str, bonelist: List[vmdstruct.VmdBoneFrame]) -> Set[int]:
	"""
	Wrapper function for the sake of organization.
	:param bonename: str name of the bone being operated on
	:param bonelist: list of all boneframes that correspond to this bone
	:return: set of ints, referring to indices within bonelist that are "important frames"
	"""
	keepset = set()
	# i'll do the x independent from the y independent from the z
	for C in range(3):  # for X, then Y, then Z:
		axis_keep_list = []
		i = 0
		while i < (len(bonelist) - 1):
			# start walking down this list
			# assume that i is the start point of a potentially over-keyed section
			b_this = bonelist[i]
			b_next = bonelist[i + 1]
			# find the delta for this channel
			b_delta = (b_next.pos[C] - b_this.pos[C]) / (b_next.f - b_this.f)
			b_sign = sign(b_delta)
			
			#+++++++++++++++++++++++++++++++++++++
			# now, walk forward from here until i "return" the frame "z" that has a different delta
			# "z" is the farthest plausible endpoint of the section (the real endpoint might be between i and z, tho)
			# "different" means only different state, i.e. rising/falling/zero
			z = 0  # to make pycharm shut up
			for z in range(i + 1, len(bonelist)):
				# if i reach the end of the bonelist, then "return" the final valid index
				if z == len(bonelist) - 1:
					break
				z_this = bonelist[z]
				z_next = bonelist[z + 1]
				z_delta = (z_next.pos[C] - z_this.pos[C]) / (z_next.f - z_this.f)
				# TODO: also break if the delta is way significantly different than the previous delta?
				#  pretty sure this concept is needed for the camera jumpcuts to be guaranteed detected?
				if sign(z_delta) == b_sign:
					pass  # if this is potentially part of the same sequence, keep iterating
				else:
					break  # if this is definitely no longer part of the sequence, THEN i can break
			# anything past z is DEFINITELY NOT the endpoint for this sequence
			# everything from i to z is monotonic: always increasing OR always decreasing OR flat zero
			# if it's flat zero, then i already know it's linear and i don't need to try to fit a curve to it lol
			if b_sign == 0:
				axis_keep_list.append(z)  # then save this proposed endpoint as a valid endpoint,
				i = z  # and move the startpoint to here and keep walking from here
				continue
			# if it hits past here, then i've got something interesting to work with!

			# OPTIMIZE: if i find z, then walk backward a bit, i can reuse the same z! no need to re-walk the same section
			while i < z:
				# +++++++++++++++++++++++++++++++++++++
				# from z, walk backward and test endpoint quality at each frame
				x_points = []
				y_points = []
				b_this = bonelist[i]
				y_start = b_this.pos[C]
				x_start = b_this.f
				# i think i want to run backwards from z until i find "an acceptably good match"
				# gonna need to do a bunch of testing to quantify what "acceptably good" looks like tho
				# TODO: no need to recompute this for each w, just use the same data and scale the bezier parameters that come out
				for w in range(z, i, -1):
					# calculate the x,y (scale of 0 to 1) for all points between i and "test"
					y_range = bonelist[w].pos[C] - y_start
					x_range = bonelist[w].f - x_start
					x_points.clear()
					y_points.clear()
					for P in range(i, w + 1):
						point = bonelist[P]
						x_rel = 127 * (point.f - x_start) / x_range
						y_rel = 127 * (point.pos[C] - y_start) / y_range
						x_points.append(x_rel)
						y_points.append(y_rel)
					# then run regression to find a reasonable interpolation curve for this stretch
					# TODO what are good error parameters to use for targets?
					#  RMSerr=2.3 and MAXerr=4.5 are pretty darn close, but could maybe be better
					#  RMSerr=9.2 and MAXerr=15.5 is TOO LARGE
					# TODO: modify to return the error values, for easier logging?
					bezier_list = vectorpaths.fit_cubic_bezier(x_points, y_points,
															   rms_err_tol=BEZIER_ERROR_THRESHOLD_BONE_POSITION_RMS,
															   max_err_tol=BEZIER_ERROR_THRESHOLD_BONE_POSITION_MAX)
					# this innately measures both the RMS error and the max error, and i can specify thresholds
					# if it cannot satisfy those thresholds it will split and try again
					# if it has split, then it's not good for my purposes
					# TODO: do something to ensure that control points are guaranteed within the box
					
					if len(bezier_list) == 1:
						# once i find a good interp curve match (if a match is found),
						if DEBUG:
							print("MATCH! bone='%s' : chan=%d : i,w,z=%d,%d,%d : sign=%d" % (
								bonename, C, i, w, z, b_sign))
						if DEBUG_PLOTS:
							bezier_list[0].plotcontrol()
							bezier_list[0].plot()
							plt.plot(x_points, y_points, 'r+')
							plt.show(block=True)
						
						axis_keep_list.append(w)  # then save this proposed endpoint as a valid endpoint,
						i = w  # and move the startpoint to here and keep walking from here
						break
					# TODO: what do i do to handle if i cannot find a good match?
					#  if i let it iterate all the way down to 2 points then it is guaranteed to find a match (cuz linear)
					#  actually it's probably also guaranteed to pass at 3 points. do i want that? hm... probably not?
					pass  # end walking backwards from z to i
				pass  # end "while i < z"
			pass  # end "while i < len(bonelist)"
		# now i have found every frame# that is important for this axis
		if DEBUG and len(axis_keep_list) > 1:
			# ignore everything that found only 1, cuz that would mean just startpoint and endpoint
			# add 1 to the length cuz frame 0 is implicitly important to all axes
			print("bone='%s' : pos : chan=%d   : keep %d/%d" % (bonename, C, len(axis_keep_list) + 1, len(bonelist)))
		# everything that this axis says needs to be kept, is stored in the set
		keepset.update(axis_keep_list)
		pass  # end for x, then y, then z
	# now i have found every frame# that is important due to position changes
	if DEBUG and len(keepset) > 1:
		# if it found only 1, ignore it, cuz that would mean just startpoint and endpoint
		# add 1 to the length cuz frame 0 is implicitly important to all axes (added to set in outer level)
		print("bone='%s' : pos : chan=ALL : keep %d/%d" % (bonename, len(keepset) + 1, len(bonelist)))
	return keepset


def _simplify_boneframes_rotation(bonename: str, bonelist: List[vmdstruct.VmdBoneFrame]) -> Set[int]:
	"""
	Wrapper function for the sake of organization.
	:param bonename: str name of the bone being operated on
	:param bonelist: list of all boneframes that correspond to this bone
	:return: set of ints, referring to indices within bonelist that are "important frames"
	"""
	keepset = set()
	i = 0
	while i < (len(bonelist) - 1):
		# start walking down this list
		# assume that i is the start point of a potentially over-keyed section
		i_this = bonelist[i]
		i_this_quat = core.euler_to_quaternion(i_this.rot)
		
		# now, walk FORWARD from here until i identify a frame z that might be an 'endpoint' of an over-key section
		y_points_all = []
		z = 0  # to make pycharm shut up
		for z in range(i + 1, min(len(bonelist), i + BONE_ROTATION_MAX_Z_LOOKAHEAD)):
			# # if i reach the end of the bonelist, then "return" the final valid index
			# if z == len(bonelist) - 1:
			# 	break
			z_this_quat = core.euler_to_quaternion(bonelist[z].rot)
			# walk forward from here, testing frames as i go
			# NEW IDEA:
			# if i can succesfully reverse-slerp everything from i to z, then z is a valid endpoint!
			# success means all reverse-slerp dimensions are close to equal
			endpoint_good = True
			temp_reverse_slerp_results = []
			temp_reverse_slerp_diffs = []
			for q in range(i + 1, z):
				# this is an exceptionally poor algorithm but idk how else to do this
				# TODO: optimize this by making a constant/cap on the number of points that i test?
				#  this currently runs in O(n^2) which is unacceptable
				#  but if i test less than every point, then my QoR will decrease...
				q_this_quat = core.euler_to_quaternion(bonelist[q].rot)
				rev = reverse_slerp(q_this_quat, i_this_quat, z_this_quat)
				# 'rev' is the slerp T-value derived from x/y/z channels of the quats... 3 values that *should* all match
				# find the greatest difference between any of these 3 values
				diff = max(math.fabs(d) for d in (rev[0]-rev[1], rev[1]-rev[2], rev[0]-rev[2]))
				temp_reverse_slerp_diffs.append(diff)
				# store this reverse-slerp T value for use later
				temp_reverse_slerp_results.append(sum(rev) / 3)
				# print(i, q, z, diff)
				if diff >= REVERSE_SLERP_TOLERANCE:
					# if any of the frames between i and z cannot be reverse-slerped, then break
					endpoint_good = False
					break
			# if DEBUG:
			# 	if temp_reverse_slerp_diffs:
			# 		m = max(temp_reverse_slerp_diffs)
			# 		print(i, z, max(temp_reverse_slerp_diffs))
			if not endpoint_good:
				# when i find something that isn't a good endpoint, then "return" the last good endpoint
				z -= 1
				break
			else:
				# if i got thru all the points between i and z, and they all passed, then this z is the last known good endpoint
				# store the reverse-slerp results for later
				y_points_all = temp_reverse_slerp_results
		
		# now i have z, and anything past z is DEFINITELY NOT the endpoint for this sequence
		# everything from i to z is "slerpable", meaning it is all falling on a linear arc
		# BUT, that doesn't mean it's all on one bezier! it might be several beziers in a row...
		# from z, walk backward and test endpoint quality at each frame!
		# the y-values are already calculated, mostly, just need to add endpoints:
		y_points_all.append(1)
		y_points_all.insert(0, 0)
		# the x-values are easy to calculate:
		x_range = bonelist[z].f - i_this.f
		x_points_all = []
		for P in range(i, z + 1):
			point = bonelist[P]
			x_rel = (point.f - i_this.f) / x_range
			x_points_all.append(x_rel)
		# now i have x_points_all and y_points_all, same length, both in range [0-1], including endpoints
		# because of slerp oddities it is possible that the y-points in the middle are outside [0-1] but thats okay i think
		assert len(x_points_all) == len(y_points_all)
		if DEBUG_PLOTS:
			print("reverse-slerp: bone='%s' : i,z=%d,%d" % (bonename, i, z))
			plt.plot(x_points_all, y_points_all, 'r+')
			plt.show(block=True)
		
		# OPTIMIZE: if i find z, then walk backward a bit and find a good bezier, i can reuse the same z!
		# no need to re-walk forward cuz i'll just find the same z-point.
		# actually, or will i? first i should try it without this optimization.
		# while i < z:
		
		# walk backwards from z until i find "an acceptably good match"... w= valid index within the points lists
		# gonna need to do a bunch of testing to quantify what "acceptably good" looks like tho
		# for w in range(z, i, -1):
		for w in range(len(x_points_all)-1, 0, -1):
			# take a subset of the range of points, and scale them to [0-128] range
			x_points = scale_list(x_points_all[0:w+1], 128)
			y_points = scale_list(y_points_all[0:w+1], 128)
			
			# then run regression to find a reasonable interpolation curve for this stretch
			# this innately measures both the RMS error and the max error, and i can specify thresholds
			# if it cannot satisfy those thresholds it will split and try again
			# TODO is this right? too tired
			bezier_list = vectorpaths.fit_cubic_bezier(x_points, y_points,
													   rms_err_tol=BEZIER_ERROR_THRESHOLD_BONE_POSITION_RMS,
													   max_err_tol=BEZIER_ERROR_THRESHOLD_BONE_POSITION_MAX)
			# TODO: do something to ensure that control points are guaranteed within the box
			
			# if it has split, then it's not good for my purposes
			# note: i modified the code so that if it would split, it returns an empty list instead
			# TODO: it would be much more efficient if i could trust/use the splitting in the algorithm, but it changes
			#  the location of the endpoints without scaling the error metrics so each split makes it easier to be
			#  accepted, even without actually fitting any better
			if len(bezier_list) != 1:
				continue
			# if any control points are not within the box, it's no good
			# (well, if its only slightly outside the box thats okay, i can clamp it)
			bez = bezier_list[0]
			cpp = (bez.p[1][0], bez.p[1][1], bez.p[2][0], bez.p[2][1])
			if not all((0-CONTROL_POINT_BOX_THRESHOLD < p < 128+CONTROL_POINT_BOX_THRESHOLD) for p in cpp):
				continue
			
			# once i find a good interp curve match (if a match is found),
			if DEBUG:
				print("MATCH! bone='%s' : i,w,z=%d,%d,%d" % (
					bonename, i, i+w, z))
			if DEBUG_PLOTS:
				bezier_list[0].plotcontrol()
				bezier_list[0].plot()
				plt.plot(x_points, y_points, 'r+')
				plt.show(block=True)
			
			keepset.add(i+w)  # then save this proposed endpoint as a valid endpoint,
			i = i+w  # and move the startpoint to here and keep walking from here
			break
			# TODO: what do i do to handle if i cannot find a good match?
			#  if i let it iterate all the way down to 2 points then it is guaranteed to find a match (cuz linear)
			#  actually it's probably also guaranteed to pass at 3 points. do i want that? hm... probably not?
			pass  # end walking backwards from z to i
		pass  # end "while i < len(bonelist)"
	# now i have found every frame# that is important due to position changes
	if DEBUG and len(keepset) > 1:
		# if it found only 1, ignore it, cuz that would mean just startpoint and endpoint
		# add 1 to the length cuz frame 0 is implicitly important to all axes (added to set in outer level)
		print("bone='%s' : rot : keep %d/%d" % (bonename, len(keepset) + 1, len(bonelist)))
	return keepset


def simplify_boneframes(allbonelist: List[vmdstruct.VmdBoneFrame]) -> List[vmdstruct.VmdBoneFrame]:
	"""
	dont yet care about phys on/off... but, eventually i should.
	only care about x/y/z/rotation
	
	:param allbonelist:
	:return:
	"""
	
	output = []
	
	# verify there is no overlapping frames, just in case
	allbonelist = vmdutil.assert_no_overlapping_frames(allbonelist)
	# sort into dict form to process each morph independently
	bonedict = vmdutil.dictify_framelist(allbonelist)
	
	# analyze each morph one at a time
	for bonename, bonelist in bonedict.items():
		print(bonename, len(bonelist))
		# if bonename != "センター": # or bonename == "左足ＩＫ":
		# 	continue
		# if bonename != "上半身": # or bonename == "左足ＩＫ":
		# 	continue
		
		if len(bonelist) <= 2:
			output.extend(bonelist)
			continue
		
		# since i need to analyze what's "important" along 4 different channels,
		# i think it's best to store a set of the indices of the frames that i think are important?
		keepset = set()
		
		# the first frame is always kept.
		keepset.add(0)
		
		#######################################################################################
		if SIMPLIFY_BONE_POSITION:
			keepset.update(_simplify_boneframes_position(bonename, bonelist))
			
		#######################################################################################
		# now, i walk along the frames analyzing the ROTATION channel. this is the hard part.
		if SIMPLIFY_BONE_ROTATION:
			keepset.update(_simplify_boneframes_rotation(bonename, bonelist))
			
		#######################################################################################
		# now done searching for the "important" points, filled "keepset"
		if DEBUG and len(keepset) > 2:
			# if it found only 2, ignore it, cuz that would mean just startpoint and endpoint
			print("bone='%s' : RESULT : keep %d/%d : keep%%=%f%%"% (
				bonename, len(keepset), len(bonelist), 100*len(keepset)/len(bonelist)))
			
		# now that i have filled the "keepidx" set, turn those into frames
		keepframe_indices = sorted(list(keepset))
		# TODO: for each of them, re-calculate the best interpolation curve for each channel based on the frames between the keepframes
		pass  # end "for each bonename, bonelist"
	return output

def main(moreinfo=True):
	###################################################################################
	# prompt for inputs
	# vmd = vmdlib.read_vmd("../../../Apple Pie_Cam-interpolated.vmd")
	vmd = vmdlib.read_vmd("../../../marionette motion 1person.vmd")
	# simplify_morphframes(vmd.morphframes)
	
	simplify_boneframes(vmd.boneframes)
	
	
	# framenums = [cam.f for cam in vmd.camframes]
	# rotx = [cam.rot[0] for cam in vmd.camframes]
	# roty = [cam.rot[1] for cam in vmd.camframes]
	# rotz = [cam.rot[2] for cam in vmd.camframes]
	# plt.plot(framenums, rotx, label="x")
	# plt.plot(framenums, roty, label="y")
	# plt.plot(framenums, rotz, label="z")
	# plt.legend()
	# plt.show()
	
	for i in range(len(vmd.camframes) - 1):
		cam = vmd.camframes[i]
		nextcam = vmd.camframes[i+1]
		rot_delta = [f - i for f,i in zip(nextcam.rot, cam.rot)]
		framedelta = nextcam.f - cam.f
		rot_delta = [r/framedelta for r in rot_delta]
		# print(cam.rot)
		try:
			r1 = rot_delta[0] / rot_delta[1]
		except ZeroDivisionError:
			r1 = 0
		try:
			r2 = rot_delta[1] / rot_delta[2]
		except ZeroDivisionError:
			r2 = 0
		try:
			r3 = rot_delta[0] / rot_delta[2]
		except ZeroDivisionError:
			r3 = 0
		if cam.f in (460, 2100, 2149):
			print('hi')
		print(cam.f, round(r1, 3), round(r2, 3), round(r3, 3))
	
	###################################################################################
	# write outputs
	#
	#
	#
	core.MY_PRINT_FUNC("")
	# output_filename_vmd = core.filepath_insert_suffix(input_filename_vmd, "_renamed")
	# output_filename_vmd = core.filepath_get_unused_name(output_filename_vmd)
	# vmdlib.write_vmd(output_filename_vmd, vmd, moreinfo=moreinfo)
	
	core.MY_PRINT_FUNC("Done!")
	return None

if __name__ == '__main__':
	core.MY_PRINT_FUNC(_SCRIPT_VERSION)
	core.MY_PRINT_FUNC(helptext)
	core.RUN_WITH_TRACEBACK(main)
	
	# x = [0] + [50]*50 + [100]
	# y = [0] + [50]*50 + [100]
	# print(vectorpaths.fit_cubic_bezier(x, y, rms_err_tol=1.0))
	
	# e1 = [0, 0, 0]
	# e2 = [0, 10, 0]
	# e3 = [0, 20, 0]
	# e4 = [43, 25, -4]
	# e5 = [43, 35, -4]
	# q1 = core.euler_to_quaternion(e1)
	# q2 = core.euler_to_quaternion(e2)
	# q3 = core.euler_to_quaternion(e3)
	# q4 = core.euler_to_quaternion(e4)
	# q5 = core.euler_to_quaternion(e5)
	#
	# d12 = get_difference_quat(q1, q2)
	# d23 = get_difference_quat(q2, q3)
	# d45 = get_difference_quat(q4, q5)
	#
	# print(d12)
	# print(d23)
	# print(d45)
	#
	# dist1 = get_quat_angular_distance(q1, q2)
	# dist2 = get_quat_angular_distance(q1, q3)
	# print(dist1)
	# print(dist2)
	# dist1 = get_quat_angular_distance(q1, q4)
	# dist2 = get_quat_angular_distance(q1, q5)
	# print(dist1)
	# print(dist2)
	# print(get_quat_angular_distance(q1, core.euler_to_quaternion((180, 0, 0))))
	# print(get_quat_angular_distance(q1, core.euler_to_quaternion((0, 180, 0))))
	# print(get_quat_angular_distance(q1, core.euler_to_quaternion((0, 0, 180))))
	# pass