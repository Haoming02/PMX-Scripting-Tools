if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main_id, test_int

helptext = '''> list_bone_children:
Given an index to a Bone, list out the chains of all its children bones

ASSERT the index of the child bone is always larger than the parent bone
'''


def recursive_print(pmx: pmxstruct.Pmx, index:int, is_top:bool):
	for i, bone in enumerate(pmx.bones[index:], start=index):

		if bone.parent_idx == index:
			core.MY_PRINT_FUNC(f'[{i}]: {bone.name_jp}')
			recursive_print(pmx, i, False)

			if is_top:
				core.MY_PRINT_FUNC('\n')

def list_bone(pmx: pmxstruct.Pmx):
	"""
	Recursively print out all bones that are the children of the Bone with the specified index
	"""

	while True:
		core.MY_PRINT_FUNC('')
		target_index = int(core.general_input(test_int, ['Index to look for: ', '[-1] to End']))
		core.MY_PRINT_FUNC('')

		if target_index < 0:
			break

		if target_index >= len(pmx.bones):
			core.MY_PRINT_FUNC('Index out of Range')
			continue

		core.MY_PRINT_FUNC(f'[{target_index}]: {pmx.bones[target_index].name_jp}\n')
		recursive_print(pmx, target_index, True)


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main_id, helptext, list_bone)
