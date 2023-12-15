"""
Math Functions used across multiple scripts
"""

from typing import Tuple, Sequence, List
import math


# ===== Fundamental Math Operations =====

def linear_map(x1: float, y1: float, x2: float, y2: float, x_in_val: float) -> float:
	"""
	Define a Y=MX+B slope via coords x1,y1 and x2,y2. Then given an X value, calculate the resulting Y.

	:param x1: x1
	:param y1: y1
	:param x2: x2
	:param y2: y2
	:param x_in_val: any float, does not need to be constrained by x1/x2
	:return: resulting Y
	"""
	m = (y2 - y1) / (x2 - x1)
	b = y2 - (m * x2)
	return x_in_val * m + b


def clamp(value: float, lower: float, upper: float) -> float:
	"""
	Basic clamp function: if below the floor, return floor; if above the ceiling, return ceiling; else return unchanged.

	:param value: float input
	:param lower: float floor
	:param upper: float ceiling
	:return: float within range [lower-upper]
	"""
	return lower if value < lower else upper if value > upper else value


def bidirectional_clamp(val: float, a: float, b: float) -> float:
	"""
	Clamp when you don't know the relative order of a and b.

	:param val: float input
	:param a: ceiling or floor
	:param b: ceiling or floor
	:return: float within range [lower-upper]
	"""
	return clamp(val, a, b) if a < b else clamp(val, b, a)


def dot(v0: Sequence[float], v1: Sequence[float]) -> float:
	"""
	Perform mathematical dot product between two same-length vectors. IE component-wise multiply, then sum.

	:param v0: any number of floats
	:param v1: same number of floats
	:return: single float
	"""
	dot = 0.0
	for (a, b) in zip(v0, v1):
		dot += a * b
	return dot


def euclidian_distance(x: Sequence[float]) -> float:
	"""
	Calculate Euclidian distance (square each component, sum, and square root).

	:param x: list/tuple, any number of floats
	:return: single float
	"""
	return math.sqrt(dot(x, x))


def normalize_distance(foo: Sequence[float]) -> List[float]:
	"""
	Normalize by Euclidian distance. Supports any number of dimensions.

	:param foo: list/tuple, any number of floats
	:return: list of floats
	"""
	LLL = euclidian_distance(foo)
	return [t / LLL for t in foo]


def normalize_sum(foo: Sequence[float]) -> List[float]:
	"""
	Normalize by sum. Supports any number of dimensions.

	:param foo: list/tuple, any number of floats
	:return: list of floats
	"""
	LLL = sum(foo)
	return [t / LLL for t in foo]


# ===== Advanced Geometric Math Functions =====

def projection(x: Sequence[float], y: Sequence[float]) -> Tuple[float,float,float]:
	"""
	Project 3D vector X onto vector Y, i.e. the component of X that is parallel with Y.

	:param x: 3x float X Y Z
	:param y: 3x float X Y Z
	:return: 3x float X Y Z
	"""
	# project x onto y:  y * (dot(x, y) / dot(y, y))
	scal = dot(x, y) / dot(y, y)
	# out = tuple(y_ * scal for y_ in y)
	return y[0]*scal, y[1]*scal, y[2]*scal


def cross_product(a: Sequence[float], b: Sequence[float]) -> Tuple[float,float,float]:
	"""
	Perform mathematical cross product between two 3D vectors.

	:param a: 3x float
	:param b: 3x float
	:return: 3x float
	"""
	return a[1]*b[2] - a[2]*b[1],\
		   a[2]*b[0] - a[0]*b[2],\
		   a[0]*b[1] - a[1]*b[0]


def quat_conjugate(q: Sequence[float]) -> Tuple[float,float,float,float]:
	"""
	"invert" or "reverse" or "conjugate" a quaternion by negating the x/y/z components.

	:param q: 4x float, W X Y Z quaternion
	:return: 4x float, W X Y Z quaternion
	"""
	return q[0], -q[1], -q[2], -q[3]


def slerp(v0: Sequence[float], v1: Sequence[float], t: float) -> Tuple[float,float,float,float]:
	"""
	Spherically Linear Interpolates between quat1 and quat2 by t.
	The param t will normally be clamped to the range [0, 1].
	If t==0, return v0; If t==1, return v1.

	:param v0: 4x float, W X Y Z quaternion
	:param v1: 4x float, W X Y Z quaternion
	:param t: float [0,1] how far to interpolate
	:return: 4x float, W X Y Z quaternion
	"""

	if math.isclose(t, 0.0, abs_tol=1e-6):
		return v0
	if math.isclose(t, 1.0, abs_tol=1e-6):
		return v1

	# If the dot product is negative, the quaternions
	# have opposite handed-ness and slerp won't take
	# the shorter path. Fix by reversing one quaternion.
	dot = dot(v0, v1)
	if dot < 0.0:
		v1 = [-v for v in v1]
		dot = -dot

	# clamp just to be safe
	dot = clamp(dot, -1.0, 1.0)

	theta = math.acos(dot)
	if theta == 0:
		# if there is no angle between the two quaternions, then interpolation is pointless
		return v0[0], v0[1], v0[2], v0[3]

	# q1 * sin((1-t) * theta) / sin(theta) + q2 * sin(t * theta) / sin(theta)
	factor0 = math.sin((1 - t) * theta) / math.sin(theta)
	factor1 = math.sin(t * theta) / math.sin(theta)
	res = tuple((v0[i] * factor0) + (v1[i] * factor1) for i in range(4))
	return res[0], res[1], res[2], res[3]


# https://en.wikipedia.org/wiki/Quaternion#Exponential,_logarithm,_and_power_functions
# https://math.stackexchange.com/questions/939229/unit-quaternion-to-a-scalar-power
# wikipedia is always good, this stackexchange thing is a bit hard to parse


def quat_ln(_q: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
	vm = euclidian_distance(_q[1:4])
	qm = euclidian_distance(_q)
	tt = (math.acos(_q[0] / qm) / vm) if (vm > 1e-9) else 0.0
	w = math.log(qm)
	return w, _q[1] * tt, _q[2] * tt, _q[3] * tt


def quat_exp(_q: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
	r = euclidian_distance(_q[1:4])
	et = math.exp(_q[0])
	s = (et * math.sin(r) / r) if (r > 1e-9) else 0.0
	w = et * math.cos(r)
	return w, _q[1] * s, _q[2] * s, _q[3] * s


def quat_pow(_q: Tuple[float, float, float, float], _n: float) -> Tuple[float, float, float, float]:
	aa = quat_ln(_q)  # pycharm type checker can go to hell
	bb = tuple(_n * i for i in aa)
	cc = quat_exp(bb)  # pycharm type checker can go to hell
	return cc


def hamilton_product(quat1: Sequence[float], quat2: Sequence[float]) -> Tuple[float,float,float,float]:
	"""
	Perform the mathematical "hamilton product", effectively adds two quaternions. However the order of the inputs does matter.
	Returns the equivalent of rotation quat2 followed by rotation quat1.
	Result is another quaternion.

	:param quat1: 4x float, W X Y Z quaternion
	:param quat2: 4x float, W X Y Z quaternion
	:return: 4x float, W X Y Z quaternion
	"""

	(a1, b1, c1, d1) = quat1
	(a2, b2, c2, d2) = quat2

	a3 = (a1 * a2) - (b1 * b2) - (c1 * c2) - (d1 * d2)
	b3 = (a1 * b2) + (b1 * a2) + (c1 * d2) - (d1 * c2)
	c3 = (a1 * c2) - (b1 * d2) + (c1 * a2) + (d1 * b2)
	d3 = (a1 * d2) + (b1 * c2) - (c1 * b2) + (d1 * a2)

	return a3, b3, c3, d3

# Special Thanks and Credit to @Isometric

def euler_to_quaternion(euler: Sequence[float]) -> Tuple[float,float,float,float]:
	"""
	Convert XYZ euler angles to WXYZ quaternion, using the same method as MikuMikuDance.
	Massive thanks and credit to "Isometric" for helping me discover the transformation method used in mmd!!!!

	:param euler: 3x float, X Y Z angle in degrees
	:return: 4x float, W X Y Z quaternion
	"""

	# angles are in degrees, must convert to radians
	roll, pitch, yaw = euler
	roll = math.radians(roll)
	pitch = math.radians(pitch)
	yaw = math.radians(yaw)

	# roll (X), pitch (Y), yaw (Z)
	sx = math.sin(roll * 0.5)
	sy = math.sin(pitch * 0.5)
	sz = math.sin(yaw * 0.5)
	cx = math.cos(roll * 0.5)
	cy = math.cos(pitch * 0.5)
	cz = math.cos(yaw * 0.5)

	w = (cz * cy * cx) + (sz * sy * sx)
	x = (cz * cy * sx) + (sz * sy * cx)
	y = (sz * cy * sx) - (cz * sy * cx)
	z = (cz * sy * sx) - (sz * cy * cx)

	return w, x, y, z


def quaternion_to_euler(quat: Sequence[float]) -> Tuple[float,float,float]:
	"""
	Convert WXYZ quaternion to XYZ euler angles, using the same method as MikuMikuDance.
	Massive thanks and credit to "Isometric" for helping me discover the transformation method used in mmd!!!!

	:param quat: 4x float, W X Y Z quaternion
	:return: 3x float, X Y Z angle in degrees
	"""

	w, x, y, z = quat

	# pitch (y-axis rotation)
	sinr_cosp = 2 * ((w * y) + (x * z))
	cosr_cosp = 1 - (2 * ((x ** 2) + (y ** 2)))
	pitch = -math.atan2(sinr_cosp, cosr_cosp)

	# yaw (z-axis rotation)
	siny_cosp = 2 * ((-w * z) - (x * y))
	cosy_cosp = 1 - (2 * ((x ** 2) + (z ** 2)))
	yaw = math.atan2(siny_cosp, cosy_cosp)

	# roll (x-axis rotation)
	sinp = 2 * ((z * y) - (w * x))
	if sinp >= 1.0:
		roll = -math.pi / 2  # use 90 degrees if out of range
	elif sinp <= -1.0:
		roll = math.pi / 2
	else:
		roll = -math.asin(sinp)

	# fixing the x rotation, part 1
	if x ** 2 > 0.5 or w < 0:
		if x < 0:
			roll = -math.pi - roll
		else:
			roll = math.pi * math.copysign(1, w) - roll

	# fixing the x rotation, part 2
	if roll > (math.pi / 2):
		roll = math.pi - roll
	elif roll < -(math.pi / 2):
		roll = -math.pi - roll

	roll = math.degrees(roll)
	pitch = math.degrees(pitch)
	yaw = math.degrees(yaw)

	return roll, pitch, yaw


def rotate3d(rotate_around: Sequence[float],
			 angle_quat: Sequence[float],
			 initial_position: Sequence[float]) -> List[float]:
	"""
	Rotate a point within 3d space around another specified point by a specific quaternion angle.

	:param rotate_around: X Y Z usually a bone location
	:param angle_quat: W X Y Z quaternion rotation to apply
	:param initial_position: X Y Z starting location of the point to be rotated
	:return: X Y Z position after rotating
	"""

	# subtract "origin" to move the whole system to rotating around 0,0,0
	point = [p - o for p, o in zip(initial_position, rotate_around)]

	length = euclidian_distance(point)
	if length != 0:
		point = [p / length for p in point]

		# set up the math as instructed by math.stackexchange
		p_vect = [0.0] + point
		r_prime_vect = quat_conjugate(angle_quat)
		# r_prime_vect = [angle_quat[0], -angle_quat[1], -angle_quat[2], -angle_quat[3]]

		# P' = R * P * R'
		# P' = H( H(R,P), R')
		temp = hamilton_product(angle_quat, p_vect)
		p_prime_vect = hamilton_product(temp, r_prime_vect)
		# note that the first element of P' will always be 0
		point = p_prime_vect[1:4]

		# might need to undo scaling the point down to unit-length???
		point = [p * length for p in point]

	# re-add "origin" to move the system to where it should have been
	point = [p + o for p, o in zip(point, rotate_around)]

	return point


def rotate2d(origin: Sequence[float], angle: float, point: Sequence[float]) -> Tuple[float,float]:
	"""
	Rotate a 2d point counterclockwise by a given angle around a given 2d origin.
	The angle should be given in radians.

	:param origin: 2x float X Y, rotate-around point
	:param angle: float, radians to rotate
	:param point: 2x float X Y, point-that-will-be-rotated
	:return: 2x float X Y, point after rotation
	"""
	ox, oy = origin
	px, py = point
	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return qx, qy


# ===== Bezier Curve Interpolation =====

class MyBezier(object):
	from bisect import bisect_left

	def __init__(self, p1: Tuple[int,int], p2: Tuple[int,int], resolution=50) -> None:
		"""
		This implements a linear approximation of a constrained Bezier curve for motion interpolation. After defining
		the control points, Y values can be easily generated from X values using self.approximate(x).

		:param p1: 2x int range [0-128], XY coordinates of control point
		:param p2: 2x int range [0-128], XY coordinates of control point
		:param resolution: int, number of points in the linear approximation of the bezier curve
		"""

		# first convert tuple(int [0-128]) to tuple(float [0.0-1.0])
		point1 = (clamp(p1[0] / 128, 0.0, 1.0), clamp(p1[1] / 128, 0.0, 1.0))
		point2 = (clamp(p2[0] / 128, 0.0, 1.0), clamp(p2[1] / 128, 0.0, 1.0))
		retlist = [(0.0, 0.0)]  # curve always starts at 0,0

		# use bezier math to create a list of XY points along the actual bezier curve, evenly spaced in t=time
		# both x-coords and y-coords are strictly increasing, but not evenly spaced
		for i in range(1, resolution):
			retlist.append(self.bezier_math(t=(i / resolution), p1=point1, p2=point2))

		retlist.append((1.0, 1.0))  # curve always ends at 1,1
		self.resolution = resolution  # store resolution param
		xx, yy = zip(*retlist)  # unzip

		self.xx = list(xx)
		self.yy = list(yy)

	def bezier_math(self, t: float, p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
		"""
		Use standard bezier equations, assuming p0=(0,0) and p3=(1,1) and p1/p2 are args, with a time value t, to calculate
		the resulting X and Y. If X/Y of p1/p2 are within range [0-1] then output X/Y are guaranteed to also be within [0-1].

		:param t: float time value
		:param p1: 2x float, coord of p1
		:param p2: 2x float, coord of p2
		:return: 2x float, resulting X Y coords
		"""

		x0, y0 = 0, 0
		x1, y1 = p1
		x2, y2 = p2
		x3, y3 = 1, 1
		x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3 * x3
		y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3 * y3

		return x, y

	def approximate(self, x: float) -> float:
		"""
		In a constrained bezier curve, X and Y have a perfect one-to-one correspondance, but the math makes it
		incredibly difficult to exactly calculate a Y given an X. So, approximate it via a series of precalculated line segments.

		:param x: float input x [0.0-1.0]
		:return: float output y [0.0-1.0]
		"""

		x = clamp(x, 0.0, 1.0)

		# first take care of the corner cases, i.e. the cases I already know the answers to:
		if x == 1.0:
			return 1.0
		elif x == 0.0:
			return 0.0

		else:
			# use binary search to find pos, the idx of the entry in self.xx which is <= x
			# if xx[3] < x < xx[4], then pos=4. so the segment starts at pos-1 and ends at pos.
			pos = self.bisect_left(self.xx, x, lo=0,	hi=len(self.xx))

		# use pos-1 and pos to get two xy points, to build a line segment, to perform linear approximation
		return linear_map(self.xx[pos-1], self.yy[pos-1],
						  self.xx[pos],   self.yy[pos],
						  x)
