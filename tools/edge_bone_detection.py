if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct
from pmx_scripting.maths import euclidian_distance

from common import main

helptext = '''> edge_bone_detection:
Identify Bones at questionable positions that may require manual fixing
'''

CENTER_THRESHOLD = 0.1
HEIGHT_THRESHOLD = 1.2
OPLIMB_THRESHOLD = 6.9
LENGTH_THRESHOLD = 8.0

ERROR = {
	'center': [],
	'height': [],
	'oplimb': [],
	'length': [],
}

def list_bone(pmx: pmxstruct.Pmx):
	"""
	Loop through all bones in a PMX model;
	print out questionable bones based on the following criteria:
	"""

	core.MY_PRINT_FUNC('')

	HEAD_Y = -1
	for bone in pmx.bones:
		if bone.name_jp.strip() == '頭':
			HEAD_Y = bone.pos[1]
			core.MY_PRINT_FUNC(f'Detected Head Height: {round(HEAD_Y, 2)}')
			OPLIMB_THRESHOLD = HEAD_Y / 2
			LENGTH_THRESHOLD = HEAD_Y / 2
			break

	for i, bone in enumerate(pmx.bones):
		x = bone.pos[0]
		y = bone.pos[1]
		z = bone.pos[2]

		# 1. Bones, other than "全ての親", at origin
		if x < CENTER_THRESHOLD and y < CENTER_THRESHOLD and z < CENTER_THRESHOLD:
			if bone.name_jp.strip() != "全ての親":
				ERROR['center'].append(f'[{i}]: {bone.name_jp.strip()}')

		# 2. Bones significantly higher than "頭"
		if HEAD_Y > 0 and y > HEAD_Y * HEIGHT_THRESHOLD:
			ERROR['height'].append(f'[{i}]: {bone.name_jp.strip()}')

		# 3. Bones too "far" in horizonal distance
		if abs(x) > OPLIMB_THRESHOLD or abs(z) > OPLIMB_THRESHOLD:
			ERROR['oplimb'].append(f'[{i}]: {bone.name_jp.strip()}')

		# 4. Bones too "long"
		if euclidian_distance(bone.tail) > LENGTH_THRESHOLD:
			ERROR['length'].append(f'[{i}]: {bone.name_jp.strip()}')


	if len(ERROR['center']) > 0:
		core.MY_PRINT_FUNC('\n===== Bones at Origin =====')
		for line in ERROR['center']:
			core.MY_PRINT_FUNC(line)

	if len(ERROR['height']) > 0:
		core.MY_PRINT_FUNC('\n===== Bones too High =====')
		for line in ERROR['height']:
			core.MY_PRINT_FUNC(line)

	if len(ERROR['oplimb']) > 0:
		core.MY_PRINT_FUNC('\n===== Bones too Far =====')
		for line in ERROR['oplimb']:
			core.MY_PRINT_FUNC(line)

	if len(ERROR['length']) > 0:
		core.MY_PRINT_FUNC('\n===== Bones too Long =====')
		for line in ERROR['length']:
			core.MY_PRINT_FUNC(line)

	core.MY_PRINT_FUNC('')
	return None, False

if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '', list_bone)
