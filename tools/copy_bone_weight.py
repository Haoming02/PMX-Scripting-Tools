if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main2, test_int

helptext = '''> copy_bone_weight:
Copy the Vertex Weights related to the specified Bone, from one model to another.
Requires inputting the mapping of the Bone index.
'''


BONE_MAPPING = {}

def validate_bone_index(pmx: pmxstruct.Pmx, i:int) -> bool:
	return 0 <= i < len(pmx.bones)

def alter_weights(source_pmx: pmxstruct.Pmx, target_pmx: pmxstruct.Pmx):
	"""
	Parse all vertex of which weights depend on the specified bone,
	then copy the weights to the target model.
	"""

	assert(len(source_pmx.verts) == len(target_pmx.verts))

	core.MY_PRINT_FUNC('')
	target_index = int(core.general_input(test_int, 'Index to look for: '))
	core.MY_PRINT_FUNC(f'[{target_index}]: {source_pmx.bones[target_index].name_jp}\n')

	is_changed = False

	for i, v in enumerate(source_pmx.verts):
		if not any(target_index == index for index, _ in v.weight):
			continue

		assert(v.weighttype == target_pmx.verts[i].weighttype)
		assert(len(v.weight) == len(target_pmx.verts[i].weight))

		for index, [bone_index, bone_ratio] in enumerate(v.weight):

			# Ask for the corresponding Bone index
			if bone_index not in BONE_MAPPING.keys():
				m_id = int(core.general_input(test_int, f'Mapped Bone for [{bone_index}] {source_pmx.bones[bone_index].name_jp}'))
				assert(validate_bone_index(target_pmx, m_id))
				BONE_MAPPING[bone_index] = m_id

			target_pmx.verts[i].weight[index] = [BONE_MAPPING[bone_index], bone_ratio]
			is_changed = True

	# Only save if something was changed
	return target_pmx, is_changed


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main2, helptext, '_weights_pasted', alter_weights)
