if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.pmx_utils import delete_multiple_bones

from common import main, sub

helptext = '''> consolidate_bones:
[for KK only]
Identify useless bones with 0 length,
link its children with its parent,
then delete it.
'''


# ===== KK Bones =====
# [..._slot$] -> [..._N_move*$] -> [..._root*$] -> [..._joint$] x N


def recur_search(pmx, index:int) -> list:
	"""
	Given an index to a Bone, return all of its children
	Always return a non-empty list of int

	ASSERT the index of children is always higher
	"""

	children = [
		i for i, bone in enumerate(pmx.bones[index:], start=index)
		if bone.parent_idx == index
	]

	assert len(children) > 0
	return children

def link_bone(pmx: pmxstruct.Pmx):

	safe = True
	to_process = []
	core.MY_PRINT_FUNC('')

	for i, SLOT in enumerate(pmx.bones):

		if '_slot' in SLOT.name_jp:

			if not SLOT.tail_usebonelink:
				try:
					children = recur_search(pmx, i)
					to_process.append((i, children))

				except AssertionError:
					core.MY_PRINT_FUNC(f'SLOT [{i}] with no Child...?')
					safe = False

				continue

			MOVE = pmx.bones[SLOT.tail]

			if '_N_move' in MOVE.name_jp:

				if not MOVE.tail_usebonelink:
					try:
						children = recur_search(pmx, SLOT.tail)
						to_process.append((i, children))

					except AssertionError:
						core.MY_PRINT_FUNC(f'MOVE [{SLOT.tail}] with no Child...?')
						safe = False

					continue

				ROOT = pmx.bones[MOVE.tail]

				if '_root' in ROOT.name_jp:

					if not ROOT.tail_usebonelink:
						try:
							children = recur_search(pmx, MOVE.tail)
							to_process.append((i, children))

						except AssertionError:
							core.MY_PRINT_FUNC(f'ROOT [{MOVE.tail}] with no Child...?')
							safe = False

						continue

					JOINT = pmx.bones[ROOT.tail]

					if '_joint' in JOINT.name_jp:

						if (ROOT.tail - i) == 3:
							to_process.append((i, [ROOT.tail]))

	if not safe:
		core.MY_PRINT_FUNC('\n^ Unsafe Issue(s) Detected...\n')
		return None, False

	if len(to_process) == 0:
		core.MY_PRINT_FUNC('\nNo Operation Needed\n')
		return None, False

	to_del = set()

	for item in to_process:
		p = item[0]
		parent_bone = pmx.bones[p]

		for c in item[1]:
			child_bone = pmx.bones[c]

			child_bone.parent_idx = parent_bone.parent_idx
			child_bone.pos = parent_bone.pos

			grandparent = pmx.bones[parent_bone.parent_idx]
			if grandparent.tail_usebonelink and grandparent.tail == p:

				if len(item[1]) > 1:
					grandparent.tail = sub(p.pos, grandparent.pos)
					grandparent.tail_usebonelink = False

				else:
					grandparent.tail = c

			to_del.add(p)

	delete_multiple_bones(pmx, list(to_del))

	core.MY_PRINT_FUNC('')
	return pmx, True


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_trimmed', link_bone)
