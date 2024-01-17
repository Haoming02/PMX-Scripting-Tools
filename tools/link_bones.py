if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.maths import euclidian_distance

from common import main

helptext = '''> link_bones:
Convert a bone's offsets into link, if the offsets fall on the position of the child bone
'''


THRESHOLD = 0.0001

def add(a:list, b:list) -> list:
	return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def sub(a:list, b:list) -> list:
	return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def on_point(a:list, b:list) -> bool:
	return euclidian_distance(sub(a, b)) < THRESHOLD

def link_bone(pmx: pmxstruct.Pmx):

	flag = False

	for i, child in reversed(list(enumerate(pmx.bones))):
		if child.parent_idx < 0 and i > 0:
			raise SystemError

		parent = pmx.bones[child.parent_idx]

		if parent.tail_usebonelink:
			continue

		if on_point(add(parent.pos, parent.tail), child.pos):
			parent.tail = [0, 0, 0]
			parent.tail = i
			parent.tail_usebonelink = True
			flag = True

	# Only save if something was changed
	return pmx, flag

if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_linked', link_bone)
