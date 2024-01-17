if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main, add, on_point

helptext = '''> link_bones:
Convert a Bone's offsets into a link, if the offsets fall on the position of the child bone
'''


def link_bone(pmx: pmxstruct.Pmx):
	"""
	Loop through all bones in a PMX model;
	calculate its offset position in relation to its child
	"""

	is_changed = False

	for i, child in reversed(list(enumerate(pmx.bones))):
		# All bones except for "全ての親" should have a parent
		if child.parent_idx < 0 and i > 0:
			raise SystemError

		parent = pmx.bones[child.parent_idx]

		if parent.tail_usebonelink:
			continue

		if on_point(add(parent.pos, parent.tail), child.pos):
			parent.tail = [0, 0, 0]
			parent.tail = i
			parent.tail_usebonelink = True
			is_changed = True

	# Only save if something was changed
	return pmx, is_changed


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_linked', link_bone)
