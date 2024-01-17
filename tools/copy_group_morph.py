if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main2
import copy

helptext = '''> copy_group_morph:
Copy Group Morphs from one model to another, based on the name of the morphs.
'''


def find_index(pmx: pmxstruct.Pmx, m_name_jp:str, m_name_en:str):
	"""
	Given the name of the morph, find the index of the morph
	Prioritize JP names
	"""
	r = -1

	for i, M in enumerate(pmx.morphs):
		if m_name_jp in M.name_jp or M.name_jp in m_name_jp:
			return i
		elif m_name_en in M.name_en or M.name_en in m_name_en:
			r = i

	return r

def parse_morph(target_pmx: pmxstruct.Pmx, source_pmx: pmxstruct.Pmx):
	"""
	Loop through all morphs in the Source PMX model,
	copy all child morphs of group morphs to the Target PMX model,
	based on the name of the morphs.
	"""

	is_changed = False

	to_copy = []
	failed = []

	for mp in source_pmx.morphs:
		if mp.morphtype is not pmxstruct.MorphType.GROUP:
			continue

		# Ignore empty group morphs
		if len(mp.items) == 0:
			continue

		dup_mp = copy.deepcopy(mp)
		success = True

		for item in dup_mp.items:
			index = item.morph_idx

			new_index = find_index(
				target_pmx,
				source_pmx.morphs[index].name_jp,
				source_pmx.morphs[index].name_en
			)

			if new_index < 0:
				success = False
				failed.append((dup_mp.name_jp, source_pmx.morphs[index].name_jp))
				break

			item.morph_idx = new_index

		# Only keep fully successfully duplicated morphs
		if success:
			to_copy.append(dup_mp)

			# Set the flag signifying that a morph was changed
			is_changed = True

	target_pmx.morphs += to_copy

	# Validate finally, just in case
	target_pmx._validate()

	if len(failed) > 0:
		core.MY_PRINT_FUNC('')
		for item in failed:
			core.MY_PRINT_FUNC(f'Failed to copy Morph: "{item[0]}"\nReason: Morph "{item[1]}" not found in Target...')
		core.MY_PRINT_FUNC('')

	# Only save if something was changed
	return target_pmx, is_changed


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main2, helptext, '_morph_pasted', parse_morph)
