if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main

helptext = '''> uniquify_names:
This function will uniquify all names of materials/bones/morphs/displayframes in the model. Bad things happen when names are not unique.
'''

# Uniquifing empty names just turns them into "*1" "*2" "*3", etc
# which is argubaly even less useful than the default "Null_01" "Null_02" "Null_03" MMD turns them into
ALSO_UNIQUIFY_NULL_NAMES = False


def uniquify_one_category(used_names: set, new_name: str) -> str:
	# translation occurred! attempt to uniquify the new name by appending *2 *3 etc
	while new_name in used_names:
		starpos = new_name.rfind("*")

		if starpos == -1:  # suffix does not exist
			new_name = new_name + "*1"

		else:  # suffix does exist
			try:
				suffixval = int(new_name[starpos + 1:])
			except ValueError:
				suffixval = 1

			new_name = new_name[:starpos] + "*" + str(suffixval + 1)

	# one leaving that loop, we finally have a unique name
	return new_name

def uniquify_names(pmx: pmxstruct.Pmx, moreinfo=False):
	"""
	uniquify the names
	return counts of how many en/jp from each category were changed
	"""

	counts = [0] * 8
	counts_labels = ["material_JP","bone_JP","morph_JP","dispframe_JP","material_EN","bone_EN","morph_EN","dispframe_EN"]

	cat_id_list = list(range(4,8))
	category_list = [pmx.materials, pmx.bones, pmx.morphs, pmx.frames]

	for cat_id, category in zip(cat_id_list, category_list):
		used_en_names = set()
		used_jp_names = set()

		for i, item in enumerate(category):
			jp_name = item.name_jp
			en_name = item.name_en
			# first, uniquify the jp name
			if jp_name != "" or ALSO_UNIQUIFY_NULL_NAMES:
				new_jp_name = uniquify_one_category(used_jp_names, jp_name)
				used_jp_names.add(new_jp_name)
				if new_jp_name != jp_name:
					if moreinfo: core.MY_PRINT_FUNC("%s: #%d    %s --> %s" % (counts_labels[cat_id - 4], i, jp_name, new_jp_name))
					# count & store into the structure
					item.name_jp = new_jp_name
					counts[cat_id - 4] += 1

			# second, uniquify the en name
			if en_name != "" or ALSO_UNIQUIFY_NULL_NAMES:
				new_en_name = uniquify_one_category(used_en_names, en_name)
				used_en_names.add(new_en_name)
				if new_en_name != en_name:
					if moreinfo: core.MY_PRINT_FUNC("%s: #%d    %s --> %s" % (counts_labels[cat_id], i, en_name, new_en_name))
					# count & store into the structure
					item.name_en = new_en_name
					counts[cat_id] += 1

	counts_dict = {x:y for x,y in zip(counts_labels, counts) if y != 0}

	if not counts_dict:
		core.MY_PRINT_FUNC("No changes are required")
		return pmx, False

	# list how many of what were changed
	core.MY_PRINT_FUNC("The following numbers in each category/language were uniquified:")
	core.MY_PRINT_FUNC(counts_dict)

	return pmx, True


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_unique', uniquify_names)
