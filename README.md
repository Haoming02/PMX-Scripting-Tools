# PMX Scripting Tools
<p align="right"><i>
Original Author: <b><a href="https://github.com/Nuthouse01/PMX-VMD-Scripting-Tools">Nuthouse01</a></b><br>
Updated by. <b>Haoming</b> - <code>2024 Jan.</code>
</i></p>

A package for reading, parsing, and modifying the data of PMX models, written in Python.
This repo also comes with a few ready-to-use tool scripts that utilize said package to improve existing models.

### Main Differences
- The core scripts were modularized and cleaned up 
- VMD-related scripts were removed
- Google Translation support is removed

### Prerequisite
- **Python**

<ins>**For simple End Users**</ins><br>
It's recommended to use the original repo, which comes with a graphical user interface instead;
unless you want to use any of the [scripts](#new-scripts) I wrote of course

<ins>**For advanced Developers**</ins><br>
Import the scripts in the `pmx_scripting` folder to easily interface with `.pmx` files

## New Scripts
- **parse_group_morph.py**: Convert `Group Morphs` into normal `Morphs` so that they are not lost when converting to other formats.
- **duplicate_group_morph.py**: Copy `Group Morphs` from one model to another, based on the name of the morphs.
- **list_bone_children.py**: List all children bones of the bone with the given index, to avoid breaking hierarchy when deleting bones.
- **list_bone_children_recuv.py**: List the chains of all children bones.
- **edge_bone_detection.py**: Identify Bones at questionable positions that may require manual fixing.
- **link_bones.py**: Convert a bone's offsets into link, if the offsets fall on the position of the child bone.
- **duplicate_bone_weight.py**: Copy Vertex Weights related to the specified Bone one model to another. Requires the mapping of the Bone index.

#### Destructive Scripts
- **precision_bone_fix.py**: Parse all out-of-place bones at a given position, and connect its children to its parent, thus removing the out-of-place bones.
- **consolidate_bones.py**: [for KK only] Remove useless zero offset bones.
