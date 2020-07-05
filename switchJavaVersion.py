import os

def main():
	print("-----------------------------")
	print("Switching Java Version")
	print("-----------------------------")
	print("")
	print("Current Java-Version:")
	print("\t" + getJava_Home())
	print("Path-Variable:")
	print("\t" + str(pathVariableToArray()))

def getJava_Home():
	java_home = ""
	try:
		java_home = os.environ['JAVA_HOME']
	except:
		java_home = "JAVA_HOME is not set!"
	return java_home

def getPathVariable():
	path = ""
	try:
		path = os.environ['Path']
	except:
		path = "Path variable is not set!"
	return path

def pathVariableToArray():
	path_variable = getPathVariable()
	if path_variable == "Path variable is not set!":
		return []
	path_array = path_variable.split(";")
	return path_array



def executeShellCommand(command):
	os.system(command)

def executeShellCommandWithOutput(command):
	return os.popen(command).read()


main()