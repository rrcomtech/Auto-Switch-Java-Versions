import os
from os import path
import shlex, subprocess
from subprocess import call
import ctypes

def main():
	print("\n-----------------------------")
	print("Switching Java Version")
	print("-----------------------------")
	print("Please run as administrator or superuser")
	print("")

	java_home = getJava_Home()

	path_variable = getPathVariable()
	paths = pathVariableToArray(path_variable)
	java_paths = getAvailableJavaPaths(paths)

	print("Available Java Versions:\n")

	printVersions(java_paths, java_home)
	print("")
	
	res = readInt("Which version do you want to switch to? (1 - " + str(len(java_paths)) + ")", 1, len(java_paths))
	print("==> " + java_paths[res - 1] + "\n")

	writable_path_var2 = ""
	counter = 0
	for i in paths:
		writable_path_var2 = writable_path_var2 + i
		if counter < (len(paths) - 2):
			writable_path_var2 = writable_path_var2 + ";"
		writable_path_var2 = writable_path_var2 + "\n"

	counter = 0
	highest_appearance = 0;
	found_one = False
	for i in paths:
		if (i in java_paths and not(found_one)):
			found_one = True
			highest_appearance = counter

		if (i == java_paths[res - 1]):
			if (not(found_one)):
				# Chosen path is already the highest ordered java path
				break;
			else:
				paths[counter] = paths[highest_appearance]
				paths[highest_appearance] = java_paths[res - 1]
				print(str(counter) + " / " + str(highest_appearance))
				break

		counter = counter + 1

	writable_path_var = ""
	counter = 0
	for i in paths:
		writable_path_var = writable_path_var + i
		if counter < (len(paths)):
			writable_path_var = writable_path_var + ";"
		writable_path_var = writable_path_var + "\n"
		counter = counter + 1

	print(writable_path_var)

	cmd = "setx -m PATH \"" + writable_path_var + "\""
	executeShellCommandWithOutput(cmd)

	cmd = "setx -m JAVA_HOME \"" + java_paths[res - 1] + "\""
	executeShellCommandWithOutput(cmd)

	subprocess.call("refreshenv", shell = True)

	print("\nDONE - Windows Users should restart their console.")


def getJava_Home():
	java_home = ""
	try:
		java_home = os.environ['JAVA_HOME']
	except:
		java_home = "JAVA_HOME is not set!"
		if checkIfAdmin():
			java_home = java_home + "\n You do not have the rights to do so! Please restart as administrator!"
		executeShellCommandWithOutput("setx -m JAVA_HOME \"\"")
	return java_home


def printVersions(java_paths, curr_java_home):
	counter = 1
	for entry in java_paths:
		
		print("(" + str(counter) + ") " + entry + ":")
		try:
			result = executeShellCommandWithOutput("\"" + entry + "\\java.exe\" -version")
		except:
			print("\t Java Version could not be found.")
		print("")

		suffix = ""
		counter = counter + 1



def getAvailableJavaPaths(paths):

	java_paths = []

	for entry in paths:
		if path.exists(entry + "\\java.exe"):
			java_paths.append(entry)

	return java_paths


def getPathVariable():
	path = ""
	try:
		path = os.environ['Path']
	except:
		path = "Path variable is not set!"
	return path


def pathVariableToArray(path_variable):
	if path_variable == "Path variable is not set!":
		return []
	path_array = path_variable.split(";")
	return path_array


def executeShellCommandWithOutput(command):
	subprocess.run(command, stdout=subprocess.PIPE)


# Reads an int and checks whether it is within two borders
def readInt(output_str, min, max):
	res = input(output_str + "\n")
	success = False

	while (not(success)):
		try:
			conv = int(res)
			if (conv <= max and conv >= min):
				success = True
			else:
				print("Number was to low or to high!")
		except:
			print("The input was not a number! Please try again.")
		
		if (not(success)):
			res = input(output_str)

	return int(res)

def checkIfAdmin():
	try:
	 	is_admin = os.getuid() == 0
	except AttributeError:
	 	is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

	return is_admin



main()
