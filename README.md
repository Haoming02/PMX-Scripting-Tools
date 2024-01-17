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
> These scripts were only written to my specific needs, and have not gone through extensive testing. They may not work on all models.
- **copy_bone_weight.py**: Copy the `Vertex Weights` related to the specified `Bone` from one model to another.
- **copy_group_morph.py**: Copy `Group Morphs` from one model to another, based on the name of the morphs.
- **edge_bone_detection.py**: Identify `Bones` at questionable positions that may require manual fixing.
- **link_bones.py**: Convert a `Bone`'s offsets into a link, if the offsets fall on the position of its child bone.
- **list_bone_children.py**: Given an index to a `Bone`, list out the chains of all its children bones.
- **parse_group_morph.py**: Convert `Group Morphs` into normal Morphs, so that they are not lost when converting to other formats.

#### Destructive Scripts
> Do **NOT** use these scripts unless you're 100% sure what they do
- **consolidate_bones.py**
- **precision_bone_fix.py**
