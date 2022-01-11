import os

def read_file(file_location):
	with open(file_location, "r") as f:
		return f.read()

def write_file(file_location, data):
	with open(file_location, "w") as f:
		f.write(data)

def file_exists(file_location):
	return os.path.isfile(file_location)

def dir_exists(dir_location):
	return os.path.isdir(dir_location)

def create_dir(location):
	os.mkdir(location)

def get_files_in_dir(dir_location):
	return [f for f in os.listdir(dir_location) if os.path.isfile(os.path.join(dir_location, f))]

def parse_save(data):
	lines = data.split("\n")
	to_return = {}
	for l in lines:
		to_return[l.split(": ")[0]] = l.split(": ")[1]
	return to_return