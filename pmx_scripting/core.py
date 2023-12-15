from typing import Tuple, Sequence, Callable, Iterable, TypeVar, Union, List, Any
from bisect import bisect_left
from os import path, listdir
import traceback
import sys

# Declare Type Hint so "output type matches whatever input type is" can be possible
THING = TypeVar('THING')


# ===== Searching through sorted lists for MASSIVE speedup =====

def binary_search_isin(x: Any, a: Sequence[Any]) -> bool:
	"""
	If x is in a, return True. Otherwise return False. a must be in ascending sorted order.
	"""

	pos = bisect_left(a, x)  # find insertion position
	return True if pos != len(a) and a[pos] == x else False  # don't walk off the end

def binary_search_wherein(x: Any, a: Sequence[Any]) -> int:
	"""
	If x is in a, return its index. Otherwise return -1. a must be in ascending sorted order.
	"""

	pos = bisect_left(a, x)  # find insertion position
	return pos if pos != len(a) and a[pos] == x else -1  # don't walk off the end


# ===== Misc Functions and User-Input Functions =====

def basic_print(*args, is_progress=False) -> None:
	"""
	CONSOLE FUNCTION: emulate built-in print() function and display text in console.
	"""

	the_string = ' '.join([str(x) for x in args])

	if is_progress:
		# leave the cursor at the beginning of the line so the next print statement overwrites this
		print(the_string, end='\r', flush=True)

	else:
		# otherwise use the normal print
		print(the_string)


PROGRESS_REFRESH_RATE = 0.05  # threshold for actually printing
PROGRESS_LAST_VALUE = 0.0  # last %
def print_progress_oneline(progress:float) -> None:
	"""
	Prints progress percentage on one continually-overwriting line. To minimize actual print-to-screen events, only
	print in increments of PROGRESS_REFRESH_RATE (5%) regardless of how often this function is called.
	This uses the MY_PRINT_FUNC approach so this function works in both GUI and CONSOLE modes.

	progress: float [0-1]
	"""

	global PROGRESS_LAST_VALUE
	# if 'curr' is lower than it was last printed (meaning reset), or it's been a while since i last printed a %, then print
	if (progress < PROGRESS_LAST_VALUE) or (progress >= PROGRESS_LAST_VALUE + PROGRESS_REFRESH_RATE):
		# cursor gets left at the beginning of line, so the next print will overwrite this one
		p = "...working: {:05.1%}".format(progress)
		MY_PRINT_FUNC(p, is_progress=True)
		PROGRESS_LAST_VALUE = progress


def my_list_search(searchme: Iterable[THING], condition: Callable[[THING], bool], getitem=False):
	# in a list of things, find the first thing where the condition is true
	for d, row in enumerate(searchme):
		if condition(row):
			return row if getitem else d

	return None


def my_list_partition(l: Iterable[THING], condition: Callable[[THING], bool]) -> Tuple[List[THING], List[THING]]:
	"""
	Split one list into two NEW lists based on a condition. Kinda like a list comprehension but it produces 2 results.

	:return: tuple of lists, (list_lambda_true, list_lambda_false)
	"""

	list_where_true = []
	list_where_false = []

	for iiiii in l:
		if condition(iiiii):
			list_where_true.append(iiiii)
		else:
			list_where_false.append(iiiii)

	return list_where_true, list_where_false

def prettyprint_file_size(size_b: int) -> str:
	"""
	Format a filesize in terms of bytes, KB, MB, GB, whatever is most appropriate.
	:param size_b: int size in bytes
	:return: string
	"""

	if abs(size_b) < 1024:
		# bytes
		ret = "%d B" % size_b

	elif abs(size_b) < 1024*1024:
		# kilobytes
		s = size_b / 1024
		ret = "{:.2f} KB".format(s)

	elif abs(size_b) < 1024*1024*1024:
		# megabytes
		s = size_b / (1024*1024)
		ret = "{:.2f} MB".format(s)

	else:
		# gigabytes
		s = size_b / (1024*1024*1024)
		ret = "{:.2f} GB".format(s)

	return ret


MAXDIFFERENCE = 0
# recursively check for equality, using a loose comparison for floatingpoints
# operating on test file, the greatest difference introduced by quaternion transform is 0.000257
# lets set sanity-check threshold at double that, 0.0005
# return the number of times a float difference exceeded the threshold
# if there is a non-float difference, return infinity
def recursively_compare(A,B):
	global MAXDIFFERENCE

	# return 1/true if it FAILS, return 0/false if it MATCHES
	if hasattr(A, "list"): A = A.list()
	if hasattr(B, "list"): B = B.list()

	if isinstance(A, float) and isinstance(B, float):
		# for floats specifically, replace exact compare with approximate compare
		diff = abs(A-B)
		MAXDIFFERENCE = max(diff, MAXDIFFERENCE)
		return diff >= 0.0005

	if isinstance(A, list) and isinstance(B, list):
		if len(A) != len(B):
			return float("inf")
		collect = 0
		for A_, B_ in zip(A, B):
			collect += recursively_compare(A_, B_)
		return collect

	# if not float and not list, then use standard compare
	if A != B:
		return float("inf")

	return None


def new_recursive_compare(L, R):
	diffcount = 0
	maxdiff = 0

	if isinstance(L, (list,tuple)) and isinstance(R, (list,tuple)):
		# if both are listlike, recurse on each element of 'em
		if len(L) != len(R):
			diffcount += 1
		# walk down both for as long as it will go, i guess?
		for d, (LL, RR) in enumerate(zip(L, R)):
			thisdiff, thismax = new_recursive_compare(LL, RR)
			diffcount += thisdiff
			maxdiff = max(maxdiff, thismax)

	elif hasattr(L,"validate") and hasattr(R,"validate"):
		# for my custom classes, look over the members with "vars" because its fancy
		Lvars = sorted(list(vars(L).items()))
		Rvars = sorted(list(vars(R).items()))
		for (nameL, LL), (nameR, RR) in zip(Lvars, Rvars):
			thisdiff, thismax = new_recursive_compare(LL, RR)
			diffcount += thisdiff
			maxdiff = max(maxdiff, thismax)

	elif isinstance(L, float) and isinstance(R, float):
		# for floats specifically, replace exact compare with approximate compare
		diff = abs(L - R)
		maxdiff = diff
		if L != R:
			diffcount += 1

	else:
		# if not float and not list, then use standard compare
		if L != R:
			diffcount += 1

	return diffcount, maxdiff


def flatten(x: Sequence) -> list:
	"""
	Recursively flatten a list of lists (or tuples). Empty lists get replaced with "None" instead of completely vanishing.
	"""
	retme = []

	for thing in x:
		if isinstance(thing, (list, tuple)):
			if len(thing) == 0:
				retme.append(None)
			else:
				retme += flatten(thing)
		else:
			retme.append(thing)

	return retme


def justify_stringlist(j: List[str], right=False) -> List[str]:
	"""
	CONSOLE FUNCTION: justify all str in a list to match the length of the longest str in that list. Determined by
	len() function, i.e. number of chars, not by true width when printed, so it doesn't work well with JP/CN chars.

	:return: list[str] after padding/justifying
	"""

	# first, look for an excuse to give up early
	if len(j) == 0 or len(j) == 1: return j
	# second, find the length of the longest string in the list
	longest_name_len = max([len(p) for p in j])
	# third, make a new list of strings that have been padded to be that length
	if right:
		# right-justify, force strings to right by padding on left
		retlist = [(" " * (longest_name_len - len(p))) + p for p in j]
	else:
		# left-justify, force strings to left by padding on right
		retlist = [p + (" " * (longest_name_len - len(p))) for p in j]

	return retlist


def prompt_user_choice(options: Sequence[int], explain_info=None) -> int:
	"""
	CONSOLE FUNCTION: prompt for multiple-choice question & continue prompting until one of those options is chosen.

	:param options: list/tuple of ints
	:param explain_info: None or str or list[str], help text that will be printed when func is called
	:return: int that the user chose
	"""

	if isinstance(explain_info, (list, tuple)):
		for p in explain_info:
			MY_PRINT_FUNC(p)

	elif isinstance(explain_info, str):
		MY_PRINT_FUNC(explain_info)

	# create set for matching against
	choicelist = [str(i) for i in options]
	# create printable string which is all options separated by slashes
	promptstr = "/".join(choicelist)

	while True:
		# continue prompting until the user gives valid input
		choice = input(" Choose [" + promptstr + "]: ")
		if choice in choicelist:
			# if given valid input, break
			break
		# if given invalid input, prompt and loop again
		MY_PRINT_FUNC("invalid choice")

	return int(choice)


def general_input(valid_check: Callable[[str], bool], explain_info=None) -> str:
	"""
	CONSOLE FUNCTION: Prompt for string input & continue prompting until given function 'valid_check' returns True.
	'valid_check' should probably print some kind of error whenever it returns False, explaining why input isn't valid.
	Trailing whitespace is removed before calling 'valid_check' and before returning result.

	:param valid_check: function or lambda that takes str as in put and returns bool
	:param explain_info: None or str or list[str], help text that will be printed when func is called
	:return: input string (trailing whitespace removed)
	"""

	if explain_info is None:
		pass
	elif isinstance(explain_info, str):
		MY_PRINT_FUNC(explain_info)
	elif isinstance(explain_info, (list, tuple)):
		for p in explain_info:
			MY_PRINT_FUNC(p)

	while True:
		s = input("> ")
		s = s.rstrip()  # no use for trailing whitespace, sometimes have use for leading whitespace
		# perform valid-check
		if valid_check(s):
			break
		else:
			# if given invalid input, prompt and loop again
			MY_PRINT_FUNC("invalid input")

	return s


def remove_quotes(input_string:str):
	"""
	When you drag a file that contains spaces in its path to the console, Windows surrounds it with quotations, which breaks the logics
	This function removes them~
	"""

	if (input_string.startswith('"') and input_string.endswith('"')) or (input_string.startswith("'") and input_string.endswith("'")):
		return input_string[1:-1]
	else:
		return input_string


def prompt_user_filename(label: str, ext_list: Union[str,Sequence[str]]) -> str:
	"""
	CONSOLE FUNCTION: prompt for file & continue prompting until user enters the name of an existing file with the
	specified file extension. Returns case-correct absolute file path to the specified file.

	:param label: {{short}} string label that identifies this kind of input, like "Text file" or "VMD file"
	:param ext_list: list of acceptable extensions, or just one string
	:return: case-correct absolute file path
	"""
	if isinstance(ext_list, str):
		# if it comes in as a string, wrap it in a list
		ext_list = [ext_list]

	MY_PRINT_FUNC('(recommended to just use absolute path)')

	while True:
		# continue prompting until the user gives valid input
		if ext_list:
			name = input("\n > {:s} path ending with [{:s}] = ".format(label, ", ".join(ext_list)))
			name = remove_quotes(name)
			valid_ext = any(name.lower().endswith(a.lower()) for a in ext_list)

			if not valid_ext:
				MY_PRINT_FUNC("Err: given file does not have acceptable extension")
				continue

		else:
			# if given an empty sequence, then do not check for valid extension. accept anything.
			name = input("  {:s} path = ".format(label))
			name = remove_quotes(name)

		if not path.isfile(name):
			MY_PRINT_FUNC("Error: given path is not a file, did you type it wrong?")
			abspath = path.abspath(name)
			# find the point where the filepath breaks! walk up folders 1 by 1 until i find the last place where the path was valid
			c = abspath
			while c and not path.exists(c):
				c = path.dirname(c)
			whereitbreaks = (" " * len(c)) + " ^^^^"
			MY_PRINT_FUNC(abspath)
			MY_PRINT_FUNC(whereitbreaks)
			continue
		break

	# it exists, so make it absolute
	name = path.abspath(path.normpath(name))

	# windows is case insensitive, so this doesn't matter, but to make it match the same case as the existing file:
	return filepath_make_casecorrect(name)


def filepath_splitdir(initial_name: str) -> Tuple[str,str]:
	"""
	Alias for path.split()
	:param initial_name: string filepath
	:return: (directories, filename)
	"""
	return path.split(initial_name)

def filepath_splitext(initial_name: str) -> Tuple[str,str]:
	"""
	Alias for path.splitext()
	:param initial_name: string filepath
	:return: (directories+filename, extension)
	"""
	return path.splitext(initial_name)

def filepath_insert_suffix(initial_name: str, suffix:str) -> str:
	"""
	Simple function, insert the suffix between the Basename and Extension.
	:param initial_name: string filepath
	:param suffix: string to append to filepath
	:return: string filepath
	"""
	N,E = filepath_splitext(initial_name)
	ret = N + suffix + E
	return ret

def filepath_make_casecorrect(initial_name: str) -> str:
	"""
	Make the given path match the case of the file/folders on the disk.
	If the path does not exist, then make it casecorrect up to the point where it no longer exists.
	:param initial_name: string filepath
	:return: string filepath, exactly the same as input except for letter case
	"""

	initial_name = path.normpath(initial_name)
	# all "." are removed, all ".." are removed except for leading...
	# first, break the given path into all of its segments
	seglist = initial_name.split(path.sep)
	if len(seglist) == 0:
		raise ValueError("ERROR: input path '%s' is too short" % initial_name)

	if path.isabs(initial_name):
		first = seglist.pop(0) + path.sep
		if path.ismount(first):
			# windows absolute path! begins with a drive letter
			reassemble_name = first.upper()
		elif first == "":
			# ???? linux ????
			reassemble_name = path.sep
		else:
			MY_PRINT_FUNC("path is abs, but doesn't start with drive or filesep? what? '%s'" % initial_name)
			reassemble_name = first
	else:
		# if not an absolute path, it needs to start as "." so that listdir works right (need to remove this when done tho)
		reassemble_name = "."

	while seglist:
		nextseg = seglist.pop(0)
		if nextseg == "..":
			reassemble_name = path.join(reassemble_name, nextseg)
		else:
			try:
				whats_here = listdir(reassemble_name)
			except FileNotFoundError:
				# fallback just in case I forgot about something
				return initial_name
			whats_here = [str(w) for w in whats_here]
			whats_here_lower = [w.lower() for w in whats_here]
			try:
				# find which entry in listdir corresponds to nextseg, when both sides are lowered
				idx = whats_here_lower.index(nextseg.lower())
			except ValueError:
				# the next segment isnt available in the listdir! the path is invalid from here on out!
				# so, just join everything remaining & break out of the loop.
				reassemble_name = path.join(reassemble_name, nextseg, *seglist)
				break
			# the next segment IS available in the listdir, so use the case-correct version of it
			reassemble_name = path.join(reassemble_name, whats_here[idx])
			# then, loop!

	# call normpath one more time to get rid of leading ".\\" when path is relative!
	reassemble_name = path.normpath(reassemble_name)
	return reassemble_name


def filepath_get_unused_name(initial_name: str, checkdisk=True, namelist=None) -> str:
	"""
	Given a desired filepath, generate a path that is guaranteed to be unused & safe to write to.
	Append integers to the end of the basename until it passes.
	Often it doesn't need to append anything and returns initial_name unmodified.

	:param initial_name: desired file path, absolute or relative.
	:param checkdisk: default True. if true, then check uniqueness against names on disk.
	:param namelist: default empty. if given, then check uniqueness against these names. list or set.
	:return: same file path as initial_name, but with integers inserted until it becomes unique (if needed)
	"""

	# if namelist is given, check against namelist as well as what's on the disk...
	# make an all-lower version of namelist
	if namelist is None: namelist_lower = []
	else:                namelist_lower = [n.lower() for n in namelist]

	basename, extension = path.splitext(initial_name)
	test_name = basename + extension  # first, try it without adding any numbers

	for append_num in range(1, 1000):
		diskpass = not (checkdisk and path.exists(test_name))
		listpass = (test_name.lower() not in namelist_lower)
		if diskpass and listpass:
			# if this name passes the disk check (or disk check is skipped), AND it passes the list check (or list is empty),
			# then this name will be kept.
			return test_name
		else:
			# if test_name is already used, then assemle a new name that includes a number
			test_name = "%s (%d)%s" % (basename, append_num, extension)

	# if it hits here, it tried 999 file names and none of them worked
	raise RuntimeError("ERROR: unable to find unused variation of '%s' for file-write" % initial_name)


def RUN_WITH_TRACEBACK(func: Callable, *args) -> None:
	"""
	Used to execute the "main" function of a script in direct-run mode.
	If it runs succesfully, do a pause-and-quit afterward.
	If an exception occurs, print the traceback info and do a pause-and-quit.
	If it was CTRL+C aborted, do not pause-and-quit.
	:param func: main-function
	:param args: optional args to pass to main-function
	"""

	try:
		MY_PRINT_FUNC("")
		func(*args)
		pause_and_quit("Done with everything! Goodbye!")

	except (KeyboardInterrupt, SystemExit):
		# this is normal and expected, do nothing and die
		pass

	except Exception as e:
		# print an error and full traceback if an exception was received!
		exc_type, exc_value, exc_traceback = sys.exc_info()
		printme_list = traceback.format_exception(e.__class__, e, exc_traceback)
		# now i have the complete traceback info as a list of strings, each ending with newline
		MY_PRINT_FUNC("")
		MY_PRINT_FUNC("".join(printme_list))
		pause_and_quit("ERROR: the script did not complete succesfully.")


# Useful as Keys for Sorting
def get1st(x):
	return x[0]

def get2nd(x):
	return x[1]


def pause_and_quit(message=None) -> None:
	"""
	CONSOLE FUNCTION: use input() to suspend until user presses ENTER
	"""

	MY_PRINT_FUNC(message)
	MY_PRINT_FUNC("...press ENTER to exit...")

	while True:
		if len(input().strip()) == 0:
			break

	raise SystemExit


if __name__ == '__main__':
	pause_and_quit("You're not supposed to run this script directly...")


# ===== Global Variable holding a Function Pointer =====
MY_PRINT_FUNC = basic_print
MY_JUSTIFY_STRINGLIST = justify_stringlist
MY_SIMPLECHOICE_FUNC = prompt_user_choice
MY_GENERAL_INPUT_FUNC = general_input
MY_FILEPROMPT_FUNC = prompt_user_filename
