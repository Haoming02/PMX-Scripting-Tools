if __name__ == '__main__':
	import sys
	import os
	sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from pmx_scripting import core
from pmx_scripting import pmx_struct as pmxstruct

from common import main

helptext = '''> alphamorph_correct:
This function fixes improper "material hide" morphs in a model. Many models simply set the opacity to 0,
but forget to zero out the edging effects or other needed fields.

To standardize "hide" morphs: when the target material is initially opaque(visible) this will change alphamorphs to use the "multiply by 0" approach; when the target is initially transparent(hidden) they will use the "add -1" approach.

To standardize "appear" morphs: when the target is initially transparent(hidden) its edge alpha will be set to 0, and the "appear" morph will add back the correct edge alpha amount.
'''


# zero-ing out tex/toon/sph alpha IS correct because the "alphamorph" PMXE plugin does it that way!
# opacity, edge size, edge alpha, tex, toon, sph
template = pmxstruct.PmxMorphItemMaterial(
	mat_idx=999, is_add=False, diffRGB=[1,1,1], specRGB=[1,1,1],ambRGB=[1,1,1], specpower=1, edgeRGB=[1,1,1],
	alpha=0, edgealpha=0, edgesize=0, texRGBA=[1,1,1,0], sphRGBA=[1,1,1,0], toonRGBA=[1,1,1,0]
)

# the above template multiplies everything by 0, the below gets the same result by subtracting 1 from everthing
template_minusone = pmxstruct.PmxMorphItemMaterial(
	mat_idx=999, is_add=True, diffRGB=[0,0,0], specRGB=[0,0,0],ambRGB=[0,0,0], specpower=0, edgeRGB=[0,0,0],
	alpha=-1, edgealpha=-1, edgesize=-1, texRGBA=[0,0,0,-1], sphRGBA=[0,0,0,-1], toonRGBA=[0,0,0,-1]
)


def alphamorph_correct(pmx: pmxstruct.Pmx, moreinfo=False):
	num_fixed = 0
	total_morphs_affected = 0

	# for each morph:
	for d,morph in enumerate(pmx.morphs):
		# if not a material morph, skip it
		if morph.morphtype != pmxstruct.MorphType.MATERIAL: continue

		this_num_fixed = 0

		# for each material in this material morph:
		for dd,matitem in enumerate(morph.items):
			# matitem:pmxstruct.PmxMorphItemMaterial  # type annotation for pycharm

			# if (mult opacity by 0) OR (add -1 to opacity), then this item is (trying to) hide the target material
			if (not matitem.is_add and matitem.alpha == 0) or (matitem.is_add and matitem.alpha == -1):
				if not (-1 <= matitem.mat_idx < len(pmx.materials)):
					core.MY_PRINT_FUNC("Warning: material morph %d item %d uses invalid material index %d, skipping" % (d, dd, matitem.mat_idx))
					continue

				# then replace the entire set of material-morph parameters
				# opacity, edge size, edge alpha, tex, toon, sph
				if matitem.mat_idx != -1 and pmx.materials[matitem.mat_idx].alpha == 0:
					# if the target material is initially transparent, replace with add-negative-1
					t = template_minusone
				else:
					# if the target material is initally opaque, or targeting the whole model, replace with mult-by-0
					t = template
				if matitem.list()[1:] != t.list()[1:]:  # if it is not already good,
					newitem = t.copy()
					newitem.mat_idx = matitem.mat_idx
					morph.items[dd] = newitem  # replace the morph with the template
					this_num_fixed += 1

		if this_num_fixed != 0:
			total_morphs_affected += 1
			num_fixed += this_num_fixed
			if moreinfo:
				core.MY_PRINT_FUNC("morph #{:<3} JP='{}' / EN='{}', fixed {} items".format(
					d, morph.name_jp, morph.name_en, this_num_fixed))

	if num_fixed:
		core.MY_PRINT_FUNC("Fixed %d 'hide' morphs" % total_morphs_affected)

	# identify materials that start transparent but still have edging
	# only transfer the EDGE ALPHA, not edge size... in some cases turning on mutiple instances of the "appear" morph
	# would cause edge size to grow bigger than planned, this is undesireable. this can also happen if the desired
	# edge alpha is <1.0 so there are still failure conditions but not transferring the edge size makes some cases better.
	mats_fixed = 0

	for d,mat in enumerate(pmx.materials):
		# if opacity is zero AND edge is enabled AND edge has nonzero opacity AND edge has nonzero size
		if mat.alpha == 0 \
				and pmxstruct.MaterialFlags.USE_EDGING in mat.matflags \
				and mat.edgealpha != 0 \
				and mat.edgesize != 0:
			this_num_edgefixed = 0

			# THEN check for any material morphs that add opacity to this material
			for d2,morph in enumerate(pmx.morphs):
				# if not a material morph, skip it
				if morph.morphtype != pmxstruct.MorphType.MATERIAL: continue
				# for each material in this material morph:
				for matitem in morph.items:
					# if not operating on the right material, skip it
					if matitem.mat_idx != d: continue
					# if adding and opacity > 0:
					if matitem.is_add and matitem.alpha > 0:
						# set it to add the edge amounts from the material
						matitem.edgealpha = mat.edgealpha
						# matitem.edgesize =  mat.edgesize
						this_num_edgefixed += 1

			# done looping over morphs
			# if it modified any locations, zero out the edge alpha in the material
			if this_num_edgefixed != 0:
				mat.edgealpha = 0
				# mat.edgesize = 0
				num_fixed += this_num_edgefixed
				mats_fixed += 1
				if moreinfo:
					core.MY_PRINT_FUNC("mat #{:<3} JP='{}' / EN='{}', fixed {} appear morphs".format(
						d, mat.name_jp, mat.name_en, this_num_edgefixed))

	if mats_fixed:
		core.MY_PRINT_FUNC("Removed edging from %d initially hidden materials" % mats_fixed)

	if num_fixed == 0 and mats_fixed == 0:
		core.MY_PRINT_FUNC("No changes are required")
		return pmx, False

	return pmx, True


if __name__ == '__main__':
	core.RUN_WITH_TRACEBACK(main, helptext, '_alphamorph', alphamorph_correct)
