if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.pmx_utils import delete_faces
import copy

from common import main

helptext = '''> prune_invalid_faces:
This script will delete any invalid faces in the model, a simple operation.
An invalid face is any face whose 3 defining vertices are not unique with respect to eachother.
This also deletes any duplicate faces within material units (faces defined by the same 3 vertices) and warns about (but doesn not fix) duplicates spanning material units.
'''


def prune_invalid_faces(pmx: pmxstruct.Pmx, moreinfo=False):
	faces_to_remove = []

	# identify faces which need removing
	for i,face in enumerate(pmx.faces):
		# valid faces are defined by 3 unique vertices, if the vertices are not unique then the face is invalid
		if 3 != len(set(face)):
			faces_to_remove.append(i)

	numinvalid = len(faces_to_remove)
	prevtotal = len(pmx.faces)

	if faces_to_remove:
		# do the actual face deletion
		delete_faces(pmx, faces_to_remove)

	if numinvalid != 0:
		core.MY_PRINT_FUNC("Found & deleted {} / {} = {:.1%} faces for being invalid".format(
			numinvalid, prevtotal, numinvalid / prevtotal))

	# NEW: delete duplicate faces within materials

	# first iter over all faces and comparable hashes from each
	# PROBLEM: faces from the same vertices but reversed are considered different faces, so sorting is not a valid way to differentiate
	# the order of the vertices within the face are what matters, but they can start from any of the 3 points
	# ABC === BCA === CAB

	# create a copy list and rotate all teh copies so that the lowest index is always first (do not modify vertex order of original!)
	facescopy = copy.deepcopy(pmx.faces)
	donothing = lambda x: x							# if i==0, don't change it
	headtotail = lambda x: x.append(x.pop(0))		# if i==1, pop the head & move it to the tail
	tailtohead = lambda x: x.insert(0, x.pop(2))	# if i==2, pop the tail & move it to the head
	opdict = {0: donothing, 1: headtotail, 2: tailtohead} # dict of functions

	for f in facescopy:
		# for each face, find the index of the minimum vert within the face
		i = f.index(min(f))
		# this can be extremely slow, for maximum efficiency use dict-lambda trick instead of if-else chain.
		# return value isn't used, the pop/append operate on the list reference
		opdict[i](f)
		# now the faces have been rotated in-place and will be saved to file

	# now the faces have been rotated so that dupes will align perfectly but mirrors will stay different!!
	# turn each face into a sorted tuple and then hash it, numbers easier to store & compare
	hashfaces = [hash(tuple(f)) for f in facescopy]

	# now make a new list where this hashed value is attached to the index of the corresponding face
	f_all_idx = list(range(len(facescopy)))
	hashfaces_idx = list(zip(hashfaces, f_all_idx))

	# for each material unit, sort & find dupes
	startidx = 0
	all_dupefaces = []

	for d,mat in enumerate(pmx.materials):
		numfaces = mat.faces_ct
		this_dupefaces = []
		# if there is 1 or 0 faces then there cannot be any dupes, so skip
		if numfaces < 2: continue
		# get the faces for this material & sort by hash so same faces are adjacent
		matfaces = hashfaces_idx[startidx : startidx+numfaces]
		matfaces.sort(key=core.get1st)
		for i in range(1,numfaces):
			# if face i is the same as face i-1,
			if matfaces[i][0] == matfaces[i-1][0]:
				# then save the index of this face
				this_dupefaces.append(matfaces[i][1])
		# always inc startidx after each material
		startidx += numfaces
		# accumulate the dupefaces between each material
		if this_dupefaces:
			all_dupefaces += this_dupefaces
			if moreinfo:
				core.MY_PRINT_FUNC("mat #{:<3} JP='{}' / EN='{}', found {} duplicates".format(
					d, mat.name_jp, mat.name_en, len(this_dupefaces)))

	# this must be in ascending sorted order
	all_dupefaces.sort()
	numdupes = len(all_dupefaces)

	# do the actual face deletion
	if all_dupefaces:
		delete_faces(pmx, all_dupefaces)

	if numdupes != 0:
		core.MY_PRINT_FUNC("Found & deleted {} / {} = {:.1%} faces for being duplicates within material units".format(
			numdupes, prevtotal, numdupes / prevtotal))

	# now find how many duplicates there are spanning material units
	# first delete the dupes we know about from the hash-list
	for f in reversed(all_dupefaces):
		hashfaces.pop(f)

	# then cast hash-list as a set to eliminate dupes and compare sizes to count how many remain
	otherdupes = len(hashfaces) - len(set(hashfaces))

	if otherdupes != 0:
		core.MY_PRINT_FUNC("Warning: Found {} faces which are duplicates spanning material units, did not delete".format(otherdupes))

	if numinvalid == 0 and numdupes == 0:
		core.MY_PRINT_FUNC("No changes are required")
		return pmx, False

	return pmx, True


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_faceprune', prune_invalid_faces)