from pmx_scripting.pmx_parser import read_pmx, write_pmx
from pmx_scripting import core

iotext = 'Inputs:  PMX file "[model].pmx"\nOutputs: PMX file "[model]{}.pmx"'

def showprompt(suffix:str):
	"""
	Ask for File Input
	"""

	core.MY_PRINT_FUNC(iotext.format(suffix))
	core.MY_PRINT_FUNC("Please enter the path to the PMX model:")

	input_filename = core.prompt_user_filename("PMX File", ".pmx")
	pmx = read_pmx(input_filename, moreinfo=True)

	return pmx, input_filename


def end(pmx, input_filename, suffix):
	"""
	Write the File Output
	"""

	output_filename = core.filepath_insert_suffix(input_filename, suffix)
	output_filename = core.filepath_get_unused_name(output_filename)
	write_pmx(output_filename, pmx, moreinfo=True)


def main(helptext:str, suffix:str, func):
	core.MY_PRINT_FUNC(helptext)

	pmx, name = showprompt(suffix)
	pmx, is_changed = func(pmx)

	if is_changed:
		end(pmx, name, suffix)

	core.pause_and_quit("Done with everything! Goodbye!")


if __name__ == '__main__':
	core.pause_and_quit("You're not supposed to run this script directly...")
