if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main, EPSILON
import copy

helptext = '''> parse_group_morph:
Convert Group Morphs into normal Morphs,
so that they are not lost when converting to other formats.
'''


def parse_morph(pmx: pmxstruct.Pmx):
	"""
	Loop through all morphs in a PMX model,
	parse the child morphs of Group Morphs, and replace the weights back onto the main morph,
	then change the type of the main morph according to its children.
	"""

	is_changed = False

	for mp in pmx.morphs:
		if mp.morphtype is not pmxstruct.MorphType.GROUP:
			continue

		# Ignore empty group morphs
		if len(mp.items) == 0:
			continue

		target_type = None
		weights_list = []

		for item in mp.items:
			index = item.morph_idx
			ratio = item.value

			child_morph = pmx.morphs[index]

			if target_type is None:
				# Identify the type of morph
				target_type = child_morph.morphtype
			else:
				# Hope no one groups multiple types of morphs together
				assert (target_type == child_morph.morphtype)

			# Ignore 0 impact entries
			if abs(ratio) < EPSILON:
				continue

			# Deep Copy to avoid stacking repeated calculation on the same morph
			child_weights = copy.deepcopy(child_morph.items)

			# Apply the Impact set in the group morph
			for ci in child_weights:

				if type(ci) == pmxstruct.PmxMorphItemVertex:
					for axis in range(3):
						ci.move[axis] *= ratio

				elif type(ci) == pmxstruct.PmxMorphItemBone:
					for axis in range(3):
						ci.move[axis] *= ratio
						ci.rot[axis] *= ratio

				elif type(ci) == pmxstruct.PmxMorphItemUV:
					for axis in range(4):
						ci.move[axis] *= ratio

				else:
					raise NotImplementedError(f'Type: {type(ci)}')

			weights_list += child_weights

		assert(target_type is not None)

		# Change the type of the main morph
		mp.morphtype = target_type

		# Apply the weights from the children
		mp.items = weights_list

		# Validate finally, just in case
		mp._validate()

		# Set the flag signifying that a morph was changed
		is_changed = True

	# Only save if something was changed
	return pmx, is_changed


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_morph_parsed', parse_morph)
