from pmx_scripting.pmx_parser import read_pmx, write_pmx
from pmx_scripting.maths import euclidian_distance
from pmx_scripting import core


EPSILON = 0.00001 # 0.001%
'''A number very close to zero'''


iotext = 'Inputs:  PMX file "[model].pmx"\nOutputs: PMX file "[model]{}.pmx"'

def showprompt(suffix:str):
	"""
	Ask for File Input
	"""

	if suffix is not None:
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
	"""
	The common function that handles the input + operation + output
	"""
	core.MY_PRINT_FUNC(helptext)

	pmx, name = showprompt(suffix)
	pmx, is_changed = func(pmx)

	if is_changed:
		end(pmx, name, suffix)

	core.pause_and_quit("Done with everything! Goodbye!")

def main_id(helptext:str, func):
	"""
	Identification variant that only queries information with no return
	"""
	core.MY_PRINT_FUNC(helptext)

	pmx, _ = showprompt(None)
	func(pmx)

	core.pause_and_quit("Goodbye!")


def showprompt2(suffix:str, is_sauce:bool):
	"""
	Ask for File Input, with source/target flag
	"""

	if suffix is not None:
		core.MY_PRINT_FUNC(iotext.format(suffix))

	if is_sauce:
		core.MY_PRINT_FUNC("Please enter the path to the Source PMX model: ")
	else:
		core.MY_PRINT_FUNC("Please enter the path to the Target PMX model: ")

	input_filename = core.prompt_user_filename("PMX File", ".pmx")
	pmx = read_pmx(input_filename, moreinfo=False)

	return pmx, input_filename

def main2(helptext:str, suffix:str, func):
	"""
	Anoter variant that takes a source and a target model instead
	"""

	core.MY_PRINT_FUNC(helptext)

	pmx1, name1 = showprompt2(None, True)

	core.MY_PRINT_FUNC('')

	pmx2, name2 = showprompt2(suffix, False)

	core.MY_PRINT_FUNC('')

	assert(name1 != name2)

	pmx, is_changed = func(pmx1, pmx2)

	if is_changed:
		end(pmx, name2, suffix)

	core.pause_and_quit("Done with everything! Goodbye!")


if __name__ == '__main__':
	core.pause_and_quit("You're not supposed to run this script directly...")


def add(a:list, b:list) -> list:
	"""
	Returns a:Vector3 + b:Vector3
	"""
	return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def sub(a:list, b:list) -> list:
	"""
	Returns a:Vector3 - b:Vector3
	"""
	return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def on_point(a:list, b:list) -> bool:
	"""
	Returns if 2 points basically have the same position
	"""
	return euclidian_distance(sub(a, b)) < EPSILON


def test_int(x:str):
	"""
	Used to validate user input
	"""
	try:
		int(x)
		return True
	except ValueError:
		return False

def test_float(x:str):
	"""
	Used to validate user input
	"""
	try:
		float(x)
		return True
	except ValueError:
		return False
