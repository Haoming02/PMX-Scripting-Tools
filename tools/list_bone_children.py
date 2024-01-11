if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main

helptext = '''> list_bone_children:
List all children bones of the bone with the given index,
to avoid breaking hierarchy when deleting bones.
'''

def test_int(x:str):
	try:
		int(x)
	except ValueError:
		return False

	return True

def list_bone(pmx: pmxstruct.Pmx):

	while True:
		core.MY_PRINT_FUNC('')
		target_index = int(core.general_input(test_int, 'Index to look for'))
		core.MY_PRINT_FUNC('')

		if target_index < 0:
			break

		if target_index >= len(pmx.bones):
			core.MY_PRINT_FUNC('Index out of Range')
			continue

		for i, bone in enumerate(pmx.bones):
			if bone.parent_idx == target_index:
				core.MY_PRINT_FUNC(f'[{i}]: {bone.name_jp}')

	return None, False

if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '', list_bone)
