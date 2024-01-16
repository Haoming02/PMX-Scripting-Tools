if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main

helptext = '''> list_bone_children_recuv:
List the chains of all children bones
ASSERT the index of the child bone is always larger than the parent
'''

def test_int(x:str):
	try:
		int(x)
	except ValueError:
		return False

	return True

def recuv_search(pmx, index, top):
	for i, bone in enumerate(pmx.bones[index:], start=index):
		if bone.parent_idx == index:
			core.MY_PRINT_FUNC(f'[{i}]: {bone.name_jp}')
			recuv_search(pmx, i, False)
			if top:
				core.MY_PRINT_FUNC('\n')

def list_bone(pmx: pmxstruct.Pmx):

	while True:
		core.MY_PRINT_FUNC('')
		target_index = int(core.general_input(test_int, 'Index to look for'))

		if target_index < 0:
			break

		if target_index >= len(pmx.bones):
			core.MY_PRINT_FUNC('Index out of Range')
			continue

		core.MY_PRINT_FUNC(f'[{target_index}]: {pmx.bones[target_index].name_jp}\n')

		recuv_search(pmx, target_index, True)

	return None, False

if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '', list_bone)
