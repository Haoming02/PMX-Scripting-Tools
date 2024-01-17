if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.maths import euclidian_distance
from pmx_scripting.pmx_utils import delete_multiple_bones

from common import main

helptext = '''> precision_bone_fix:
Parse all out-of-place bones at a given position,
and connect its children to its parent,
thus removing the out-of-place bones.
'''


THRESHOLD = 0.0001

def sub(a:list, b:list) -> list:
	return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def on_point(a:list, b:list) -> bool:
	return euclidian_distance(sub(a, b)) < THRESHOLD

def test_int(x:str):
	try:
		int(x)
	except ValueError:
		return False

	return True

def test_float(x:str):
	try:
		float(x)
	except ValueError:
		return False

	return True

def is_zeroOffset(pmx, bone) -> bool:
	if bone.tail_usebonelink:
		return euclidian_distance(sub(bone.pos, pmx.bones[bone.tail].pos)) < THRESHOLD
	else:
		return euclidian_distance(bone.tail) < THRESHOLD

def recuv_search(pmx, index):
	children = [
		i for i, bone in enumerate(pmx.bones[index:], start=index)
		if bone.parent_idx == index
	]

	assert len(children) > 0
	return children

def trace_parent(pmx, bone, target):
	limit = 5
	parent = pmx.bones[bone.parent_idx]

	while parent.parent_idx != target:
		parent = pmx.bones[parent.parent_idx]
		limit -= 1

		if limit == 0:
			raise SystemError

	return pmx.bones.index(parent)

def trace_children(pmx, bone):
	if is_zeroOffset(pmx, bone):
		return [pmx.bones.index(bone)]

	if bone.tail_usebonelink:
		return trace_children(pmx, pmx.bones[bone.tail])

	else:
		children = recuv_search(pmx, pmx.bones.index(bone))

		for c in children:
			assert(is_zeroOffset(pmx, pmx.bones[c]))

		return children

def fix_bones(pmx: pmxstruct.Pmx):

	core.MY_PRINT_FUNC('')
	target = [
		float(core.general_input(test_float, 'X:')),
		float(core.general_input(test_float, 'Y:')),
		float(core.general_input(test_float, 'Z:'))
	]
	core.MY_PRINT_FUNC('')

	common = int(core.general_input(test_int, 'Common Index:'))

	to_del = set()

	for i, bone in enumerate(pmx.bones):
		if not on_point(target, bone.pos):
			continue

		parent = trace_parent(pmx, bone, common)
		children = trace_children(pmx, bone)

		for child in children:
			pmx.bones[child].pos = pmx.bones[parent].pos
			pmx.bones[child].parent_idx = common

			assert(parent <= i <= child)

		for d in range(parent, min(children)):
			to_del.add(d)

	to_del = sorted(list(to_del))

	for v in pmx.verts:
		for pair in v.weight:
			if pair[0] in to_del:
				pair[0] = common

	delete_multiple_bones(pmx, to_del)

	#core.MY_PRINT_FUNC('')
	#return None, False
	return pmx, True

if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_precision', fix_bones)
