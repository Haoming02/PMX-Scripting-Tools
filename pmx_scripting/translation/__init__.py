"""
Translation-Related Scripts

Original Dictionaries by. Nuthouse01

For non-standard words, just use ChatGPT...

Usage:
from translation import translate
"""

from .translation_functions import pre_translate, piecewise_translate, is_latin
from .translation_dictionaries import words_dict

def translate(in_list: str, DEBUG:bool = False) -> str:
	"""
	Simple wrapper function to run both pre_translate and local_translate using words_dict.

	Accepts List of String as well~
	"""

	input_is_str = isinstance(in_list, str)
	if input_is_str: in_list = [in_list]

	# first, run pretranslate: take care of the standard stuff
	# things like prefixes, suffixes, fullwidth alphanumeric characters, etc
	indents, bodies, suffixes = pre_translate(in_list)

	# second, run piecewise translation with the hardcoded "words dict"
	outbodies = piecewise_translate(bodies, words_dict)

	# third, reattach the indents and suffixes
	outlist = [i + b + s for i,b,s in zip(indents, outbodies, suffixes)]

	# pretty much done!

	if DEBUG:
		print("Localtranslate Results:")
		for s,o in zip(in_list, outlist):
			print("%d :: %s :: %s" % (is_latin(o), s, o))

	if input_is_str:
		return outlist[0]
	else:
		return outlist
