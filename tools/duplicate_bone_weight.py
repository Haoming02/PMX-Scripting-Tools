if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.pmx_parser import read_pmx, write_pmx

helptext = '''> duplicate_bone_weight:
Copy Vertex Weights related to the specified Bone one model to another.
Requires the mapping of the Bone index.
'''


BONE_MAPPING = {}

def test_int(x:str) -> bool:
	try:
		int(x)
	except ValueError:
		return False

	return True

def validate_bone_index(x:int, target_pmx) -> bool:
	return 0 <= x < len(target_pmx.bones)

def alter_weights(source_pmx: pmxstruct.Pmx, target_pmx: pmxstruct.Pmx):

	assert(len(source_pmx.verts) == len(target_pmx.verts))

	core.MY_PRINT_FUNC('')
	target_index = int(core.general_input(test_int, 'Index to look for: '))
	core.MY_PRINT_FUNC(f'[{target_index}]: {source_pmx.bones[target_index].name_jp}\n')

	for i, v in enumerate(source_pmx.verts):
		flag = any(target_index == index for index, _ in v.weight)

		if flag:
			assert(v.weighttype == target_pmx.verts[i].weighttype)
			assert(len(v.weight) == len(target_pmx.verts[i].weight))

			for index, [bone_index, bone_ratio] in enumerate(v.weight):

				if bone_index not in BONE_MAPPING.keys():
					m_id = int(core.general_input(test_int, f'Mapped Bone for [{bone_index}] {source_pmx.bones[bone_index].name_jp}'))
					assert(validate_bone_index(m_id, target_pmx))
					BONE_MAPPING[bone_index] = m_id

				target_pmx.verts[i].weight[index] = [BONE_MAPPING[bone_index], bone_ratio]

	return target_pmx, True


# ===== Custom Commons =====
def showprompt(suffix:str, sauce:bool):
	"""
	Ask for File Input
	"""

	core.MY_PRINT_FUNC(f'Inputs:  PMX file "[model].pmx"\nOutputs: PMX file "[model]{suffix}.pmx"')

	if sauce:
		core.MY_PRINT_FUNC("Please enter the path to the Source PMX model:")
	else:
		core.MY_PRINT_FUNC("Please enter the path to the Target PMX model:")

	input_filename = core.prompt_user_filename("PMX File", ".pmx")
	pmx = read_pmx(input_filename, moreinfo=False)

	return pmx, input_filename

def end(pmx, input_filename, suffix):
	"""
	Write the File Output
	"""

	output_filename = core.filepath_insert_suffix(input_filename, suffix)
	output_filename = core.filepath_get_unused_name(output_filename)
	write_pmx(output_filename, pmx, moreinfo=True)

def main(helptext:str, suffix:str, func):
	"""
	Rewrite again instead of using commons to implement additional logics
	"""

	core.MY_PRINT_FUNC(helptext)

	pmx1, name1 = showprompt(suffix, True)

	core.MY_PRINT_FUNC('')

	pmx2, name2 = showprompt(suffix, False)

	core.MY_PRINT_FUNC('')

	assert(name1 != name2)

	pmx, is_changed = func(pmx1, pmx2)

	if is_changed:
		end(pmx, name2, suffix)

	core.pause_and_quit("Done with everything! Goodbye!")
# ===== Custom Commons =====


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_bones_added', alter_weights)
