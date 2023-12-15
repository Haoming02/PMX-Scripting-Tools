if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.pmx_utils import delme_list_to_rangemap, vert_delete_and_remap

from common import main

helptext = '''> prune_unused_vertices:
This script will delete any unused vertices from the model, sometimes causing massive file size improvements.
An unused vertex is one which is not used to define any faces.
'''


def prune_unused_vertices(pmx: pmxstruct.Pmx, moreinfo=False):
	"""
	Vertices are referenced in faces, morphs (uv and vertex morphs), and soft bodies (should also be handled)

	find individual vertices to delete
		build set of vertices used in faces
		build set of all vertices (just a range)
		subtract
		convert to sorted list
	convert to list of [begin, length]
		iterate over delvertlist, identify contiguous blocks
	convert to list of [begin, cumulative size]
	"""

	# build set of USED vertices
	used_verts = set()

	for face in pmx.faces:
		used_verts.update(face)

	# build set of ALL vertices
	all_verts = set(list(range(len(pmx.verts))))
	# derive set of UNUSED vertices by subtracting
	unused_verts = all_verts.difference(used_verts)
	# convert to ordered list
	delme_verts = sorted(list(unused_verts))

	numdeleted = len(delme_verts)
	prevtotal = len(pmx.verts)

	if numdeleted == 0:
		core.MY_PRINT_FUNC("No changes are required")
		return pmx, False

	delme_range = delme_list_to_rangemap(delme_verts)

	if moreinfo:
		core.MY_PRINT_FUNC("Detected %d orphan vertices arranged in %d contiguous blocks" % (len(delme_verts), len(delme_range[0])))

	vert_delete_and_remap(pmx, delme_verts, delme_range)

	core.MY_PRINT_FUNC("Identified and deleted {} / {} = {:.1%} vertices for being unused".format(
		numdeleted, prevtotal, numdeleted/prevtotal))

	return pmx, True


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_vertprune', prune_unused_vertices)
