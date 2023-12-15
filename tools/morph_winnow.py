if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.pmx_utils import delme_list_to_rangemap, morph_delete_and_remap
from pmx_scripting.maths import euclidian_distance

from common import main

helptext = '''> morph_winnow:
To reduce overall file size, this will delete vertices from vertex morphs that move imperceptibly small distances.
This will also delete any vertex morphs that have all of their controlled vertices deleted this way.
The default threshold is 0.00032 units.
'''


DELETE_NEWLY_EMPTIED_MORPHS = True

# a vertex is removed from a morph if its total deformation is below this value
WINNOW_THRESHOLD = 0.00032

# these are morphs used for controlling AutoLuminous stuff, they generally are vertex morphs that contain 1-3 vertices
# with offsets of 0,0,0, but they shouldn't be deleted
IGNORE_THESE_MORPHS = [
	"LightUp",
	"LightOff",
	"LightBlink",
	"LightBS",
	"LightUpE",
	"LightDuty",
	"LightMin",
	"LClockUp",
	"LClockDown",
]


def morph_winnow(pmx: pmxstruct.Pmx, moreinfo=False):
	total_num_verts = 0
	total_vert_dropped = 0
	total_morphs_affected = 0

	morphs_now_empty = []

	# for each morph:
	for d,morph in enumerate(pmx.morphs):
		# if not a vertex morph, skip it
		if morph.morphtype != pmxstruct.MorphType.VERTEX: continue
		# if it has one of the special AutoLuminous morph names, then skip it
		if morph.name_jp in IGNORE_THESE_MORPHS: continue
		# for each vert in this vertex morph:
		i = 0
		this_vert_dropped = 0  # lines dropped from this morph
		total_num_verts += len(morph.items)
		while i < len(morph.items):
			vert = morph.items[i]
			vert:pmxstruct.PmxMorphItemVertex
			# determine if it is worth keeping or deleting
			# first, calculate euclidian distance
			length = euclidian_distance(vert.move)
			if length < WINNOW_THRESHOLD:
				morph.items.pop(i)
				this_vert_dropped += 1
			else:
				i += 1
		if len(morph.items) == 0:
			# mark newly-emptied vertex morphs for later removal
			morphs_now_empty.append(d)
		# increment tracking variables
		if this_vert_dropped != 0:
			if moreinfo:
				core.MY_PRINT_FUNC("morph #{:<3} JP='{}' / EN='{}', removed {} vertices".format(
					d, morph.name_jp, morph.name_en, this_vert_dropped))
			total_morphs_affected += 1
			total_vert_dropped += this_vert_dropped

	if total_vert_dropped == 0:
		core.MY_PRINT_FUNC("No changes are required")
		return pmx, False

	core.MY_PRINT_FUNC("Dropped {} / {} = {:.1%} vertices from among {} affected morphs".format(
		total_vert_dropped, total_num_verts, total_vert_dropped/total_num_verts, total_morphs_affected))

	if morphs_now_empty and DELETE_NEWLY_EMPTIED_MORPHS:
		core.MY_PRINT_FUNC("Deleted %d morphs that had all of their vertices below the threshold" % len(morphs_now_empty))
		rangemap = delme_list_to_rangemap(morphs_now_empty)

		morph_delete_and_remap(pmx, morphs_now_empty, rangemap)

	return pmx, True


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_winnow', morph_winnow)
