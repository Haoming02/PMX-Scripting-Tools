if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.pmx_parser import read_pmx, write_pmx

import copy

helptext = '''> duplicate_group_morph:
Copy Group Morphs from one model to another, based on the name of the morphs.
'''


def find_index(target_pmx: pmxstruct.Pmx, m_name_jp:str, m_name_en:str):
	"""
	Given the name of the morph, find the index of the morph
	Prioritize JP names
	"""

	l = len(target_pmx.morphs)
	for i in range(l):
		if m_name_jp in target_pmx.morphs[i].name_jp or target_pmx.morphs[i].name_jp in m_name_jp:
			return i

	for i in range(l):
		if m_name_en in target_pmx.morphs[i].name_en or target_pmx.morphs[i].name_en in m_name_en:
			return i

	return -1

def parse_morph(target_pmx: pmxstruct.Pmx, source_pmx: pmxstruct.Pmx, insert:bool):
	"""
	Loop through all morphs in the Source PMX model; for group morphs,
	copy its child morphs to the Target PMX model, based on the name of the morphs.
	"""

	is_changed = False
	to_copy = []
	failed = []

	for mp in source_pmx.morphs:
		if mp.morphtype == pmxstruct.MorphType.GROUP:

			# Ignore empty group morphs
			if len(mp.items) == 0:
				continue

			dup_mp = copy.deepcopy(mp)
			flag = True

			for item in dup_mp.items:
				index = item.morph_idx

				new_index = find_index(
					target_pmx,
					source_pmx.morphs[index].name_jp,
					source_pmx.morphs[index].name_en
				)

				if new_index < 0:
					flag = False
					failed.append((dup_mp.name_jp, source_pmx.morphs[index].name_jp))
					break

				item.morph_idx = new_index

			# Only keep fully successfully duplicated morphs
			if flag:
				to_copy.append(dup_mp)

				# Set the flag signifying that a morph was changed
				is_changed = True

	if insert:
		shift = len(to_copy)

		# Since the ID is index-based, if you insert from the start, the index of the morphs will be shifted further
		for mp in to_copy:
			for item in mp.items:
				item.morph_idx += shift

		target_pmx.morphs[0:0] = to_copy

	else:
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

	pmx1, name1 = showprompt(suffix, False)

	core.MY_PRINT_FUNC('')

	pmx2, name2 = showprompt(suffix, True)

	assert(name1 != name2)

	core.MY_PRINT_FUNC('')
	insert = core.general_input(lambda x: x in ('y', 'n'), ['Insert from the beginning?', '[y/n]'])

	pmx, is_changed = func(pmx1, pmx2, insert == 'y')

	if is_changed:
		end(pmx, name1, suffix)

	core.pause_and_quit("Done with everything! Goodbye!")
# ===== Custom Commons =====


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_morph_added', parse_morph)
