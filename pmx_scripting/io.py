from .core import MY_PRINT_FUNC

from typing import Any, List
from os import path
import stat
import csv
import os


# ===== Functions for CSV and Binary-File read/write =====

def write_csvlist_to_file(dest_path:str, content:List[List[Any]], use_jis_encoding=False, quiet=False) -> None:
	"""
	Receive a list-of-lists format and write it to textfile on disk in CSV format.

	:param dest_path: destination file path, as a string, relative from CWD or absolute
	:param content: list-of-lists format, OR list-of-strings format
	:param use_jis_encoding: by default, assume utf-8 encoding. if this=True, use shift_jis instead.
	:param quiet: by default, print the absolute path being written to. if this=True, don't do this.
	"""

	# replace csv.writer with my own convert-to-csv block to get the escaping behavior i needed
	# when PMXE writes a CSV, it backslash-escapes backslashes and dots and spaces, but it doesn't need these to be escaped when reading
	# also, doublequotes are escaped with an additional doublequote
	# also, strings are wrapped in doublequotes if it contains any doublequotes, contains any commas, or starts or ends with whitespace
	buildme = []

	for line in content:
		newline = []
		if isinstance(line, str):  # if it is already a string, don't do anything fancy, just use it
			newline_str = line
		else:  # if it is not a string, it should be a list or tuple, so iterate over it
			for item in line:
				# check if it needs special treatment, apply if needed
				if isinstance(item, str):
					# make a copy so I am not modifying the input list
					newstr = item
					# first, escape all doublequotes with more doublequotes
					newstr.replace('"', '""')
					# then check if the whole thing needs wrapped:
					# contains any doublequotes, contains any commas, or starts or ends with whitespace
					if ('"' in newstr) or (',' in newstr) or (len(newstr) > 0 and (newstr[0].isspace() or newstr[-1].isspace())):
						newstr = '"%s"' % newstr
					newline.append(newstr)
				else:
					# convert to string & append onto newline
					newline.append(str(item))
			# done with this line: join the items with commas
			newline_str = ",".join(newline)
		# whether line was string or was list, it is now converted to string & can be appended
		buildme.append(newline_str)
	# # add this so it has one empty line at the end just cuz
	# buildme.append("")

	# do actual write-to-disk
	write_list_to_txtfile(dest_path, buildme, use_jis_encoding=use_jis_encoding, quiet=quiet)

	return None


def read_file_to_csvlist(src_path:str, use_jis_encoding=False, quiet=False) -> List[List[Any]]:
	"""
	Read a CSV text file from disk & return a type-correct list-of-lists format

	:param src_path: source file path, as a string, relative from CWD or absolute
	:param use_jis_encoding: by default, assume utf-8 encoding. if this=True, use shift_jis instead.
	:param quiet: by default, print the absolute path being written to. if this=True, don't do this.
	:return: list-of-lists format
	"""

	# do actual read-from-disk & split at line breaks
	rb_list = read_txtfile_to_list(src_path, use_jis_encoding=use_jis_encoding, quiet=quiet)

	# use stock CSV reader to handle unescaping stuff & break each line into a list of fields
	# 'csv_content' is now list-of-lists format, but is not yet type-correct, each item is strings
	reader = csv.reader(rb_list, delimiter=',', quoting=csv.QUOTE_ALL)
	csv_content = []
	try:
		for row in reader:
			csv_content.append(row)

	except csv.Error as e:
		MY_PRINT_FUNC(e.__class__.__name__, e)
		MY_PRINT_FUNC("ERROR: malformed CSV format in the text file prevented parsing from text to list form, check your commas")
		MY_PRINT_FUNC("file '{}', line #{}".format(src_path, reader.line_num))
		MY_PRINT_FUNC("input line = '{}'".format(rb_list[reader.line_num]))
		raise

	# ideally the csv reader should detect what type each thing is but the encoding is making it all fucky
	# so, just read everything in as a string i guess, then build a new list 'data' where all the types are correct
	data = []

	for row in csv_content:
		newrow = []

		for item in row:
			# manual type conversion: everything in the document is either int,float,bool,string
			# is it an integer?
			try:
				newrow.append(int(item))
				continue
			except ValueError:
				pass
			# is it a float?
			try:
				newrow.append(float(item))
				continue
			except ValueError:
				pass
			# is it a bool?
			if item.lower() == "true":
				newrow.append(True)
				continue
			if item.lower() == "false":
				newrow.append(False)
				continue
			# is it a none?
			if item == "None":
				newrow.append(None)
				continue
			# i guess its just a string, then. keep it unchanged
			newrow.append(item)

		data.append(newrow)

	return data


def write_list_to_txtfile(dest_path: str, content: List[str], use_jis_encoding=False, quiet=False) -> None:
	"""
	WRITE a list of strings from memory into a TEXT file.

	:param dest_path: destination file path, as a string, relative from CWD or absolute
	:param content: list of lines, each line is a string
	:param use_jis_encoding: by default, assume utf-8 encoding. if this=True, use shift_jis instead.
	:param quiet: by default, print the absolute path being written to. if this=True, don't do this.
	"""

	writeme = "\n".join(content)
	write_str_to_txtfile(dest_path, writeme, use_jis_encoding=use_jis_encoding, quiet=quiet)
	return None


def write_bytes_to_binfile(dest_path:str, content:bytearray, quiet=False) -> None:
	"""
	WRITE a BINARY file from memory to disk.

	:param dest_path: destination file path, as a string, relative from CWD or absolute
	:param content: bytearray obj or bytes obj
	:param quiet: by default, print the absolute path being written to. if this=True, don't do this.
	"""

	dest_path = path.abspath(path.normpath(dest_path))
	# unless disabled, print the absolute path to the file being written
	if not quiet: MY_PRINT_FUNC(dest_path)

	# assert that the destination folder exists
	if not path.exists(path.dirname(dest_path)):
		raise RuntimeError("ERROR: unable to write binary file '%s', the containing folder(s) do not exist!" % dest_path)

	# check if it is okay to write to this dest name
	if path.exists(dest_path):
		if not path.isfile(dest_path):
			# don't want to overwrite a folder with a file, that would be bad
			raise RuntimeError("ERROR: unable to write binary file '%s', the dest name already exists as a non-file object!" % dest_path)
		else:
			if not quiet: MY_PRINT_FUNC("WARNING: binary file '%s' already exists, I am going to overwrite it!" % dest_path)
			# the file exists already and is about to be overwritten, check whether it is set to read-only?
			check_and_fix_readonly(dest_path)

	try:
		with open(dest_path, "wb") as my_file:  # w = write, b = binary
			my_file.write(content)  # plain old no-frills write
	except IOError as e:
		MY_PRINT_FUNC(e.__class__.__name__, e)
		MY_PRINT_FUNC("ERROR: unable to write binary file '%s', maybe its a permissions issue?" % dest_path)
		raise

	return None


def read_binfile_to_bytes(src_path:str, quiet=False) -> bytearray:
	"""
	READ a BINARY file from disk into memory.

	:param src_path: source file path, as a string, relative from CWD or absolute
	:param quiet: by default, print the absolute path being written to. if this=True, don't do this.
	:return: bytearray obj
	"""

	src_path = path.abspath(path.normpath(src_path))

	# unless disabled, print the absolute path to the file being read
	if not quiet: MY_PRINT_FUNC(src_path)

	# assert that the given path exists and is a file, not a folder
	if not path.isfile(src_path):
		raise RuntimeError("ERROR: attempt to read binary file '%s', but it does not exist! (or exists but is not a file)" % src_path)

	try:
		with open(src_path, mode='rb') as file:  # r=read, b=binary
			raw = file.read()  # plain old no-frills dump file from disk to memory
	except IOError as e:
		MY_PRINT_FUNC(e.__class__.__name__, e)
		MY_PRINT_FUNC("ERROR: error wile reading binary file '%s', maybe you typed it wrong?" % src_path)
		raise

	return bytearray(raw)


def write_str_to_txtfile(dest_path: str, content: str, use_jis_encoding=False, quiet=False) -> None:
	"""
	WRITE a string from memory to a TEXT file.

	:param dest_path: destination file path, as a string, relative from CWD or absolute
	:param content: list of lines, each line is a string
	:param use_jis_encoding: by default, assume utf-8 encoding. if this=True, use shift_jis instead.
	:param quiet: by default, print the absolute path being written to. if this=True, don't do this.
	"""

	dest_path = path.abspath(path.normpath(dest_path))

	# unless disabled, print the absolute path to the file being read
	if not quiet: MY_PRINT_FUNC(dest_path)

	# assert that the destination folder exists
	if not path.exists(path.dirname(dest_path)):
		raise RuntimeError("ERROR: unable to write text file '%s', the containing folder(s) do not exist!" % dest_path)

	# check if it is okay to write to this dest name
	if path.exists(dest_path):
		if not path.isfile(dest_path):
			# don't want to overwrite a folder with a file, that would be bad
			raise RuntimeError("ERROR: unable to write text file '%s', the dest name already exists as a non-file object!" % dest_path)
		else:
			if not quiet: MY_PRINT_FUNC("WARNING: text file '%s' already exists, I am going to overwrite it!" % dest_path)
			# the file exists already and is about to be overwritten, check whether it is set to read-only?
			check_and_fix_readonly(dest_path)

	# default encoding is utf-8, but use shift_jis if use_jis_encoding is True
	enc = "shift_jis" if use_jis_encoding else "utf-8"

	try:
		with open(dest_path, "wt", encoding=enc, errors="strict") as my_file:  # w=write, t=text
			my_file.write(content)  # plain old no-frills write
	except UnicodeEncodeError as e:
		MY_PRINT_FUNC(e.__class__.__name__, e)
		MY_PRINT_FUNC("ERROR: attempt to write text file '%s', but encoding '%s' could not handle contents!" % (dest_path, enc))
		raise
	except IOError as e:
		MY_PRINT_FUNC(e.__class__.__name__, e)
		MY_PRINT_FUNC("ERROR: unable to write text file '%s', maybe its a permissions issue?" % dest_path)
		raise

	return None


def read_txtfile_to_list(src_path:str, use_jis_encoding=False, quiet=False) -> List[str]:
	"""
	READ a TEXT file from disk into memory.

	:param src_path: source file path, as a string, relative from CWD or absolute
	:param use_jis_encoding: by default, assume utf-8 encoding. if this=True, use shift_jis instead.
	:param quiet: by default, print the absolute path being written to. if this=True, don't do this.
	:return: list of lines, each line is a string
	"""

	src_path = path.abspath(path.normpath(src_path))
	# unless disabled, print the absolute path to the file being read
	if not quiet: MY_PRINT_FUNC(src_path)

	# assert that the given path exists and is a file, not a folder
	if not path.isfile(src_path):
		raise RuntimeError("ERROR: attempt to read text file '%s', but it does not exist! (or exists but is not a file)" % src_path)

	# default encoding is utf-8, but use shift_jis if use_jis_encoding is given
	enc = "shift_jis" if use_jis_encoding else "utf-8"

	try:
		with open(src_path, "rt", encoding=enc, errors="strict") as my_file:  # r=read, t=text
			rb_unicode = my_file.read()
	except UnicodeDecodeError as e:
		MY_PRINT_FUNC(e.__class__.__name__, e)
		MY_PRINT_FUNC("ERROR: attempt to read text file '%s', but encoding '%s' could not handle contents!" % (src_path, enc))
		raise
	except IOError as e:
		MY_PRINT_FUNC(e.__class__.__name__, e)
		MY_PRINT_FUNC("ERROR: error wile reading text file '%s', maybe you typed it wrong?" % src_path)
		raise

	# break rb_unicode into a list object at standard line endings and return
	return rb_unicode.splitlines()


def check_and_fix_readonly(filepath: str) -> None:
	# the file exists already and is about to be overwritten, check whether it is set to read-only?
	if not os.access(filepath, os.W_OK):
		MY_PRINT_FUNC(
			"WARNING: file '%s' currently set to READ-ONLY, but I want to overwrite it so I am going to change its permissions!" % filepath)
		current_permissions = stat.S_IMODE(os.lstat(filepath).st_mode)
		ALL_WRITE_PERMISSION = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
		os.chmod(filepath, current_permissions | ALL_WRITE_PERMISSION)

	return
