import os
rootdir = '/Users/work/development/repositories/pet-projects'

languageDirectories = next(os.walk(rootdir))[1]

if not os.path.islink("all"):
	os.symlink(rootdir, "all")
else:
	print "Link to ", "all", "exists already"

for directory in languageDirectories:
	if(directory.startswith(".")):
		continue;

	projectDirectories = next(os.walk(rootdir + "/" + directory))[1]
	for projectDir in projectDirectories:
		fullProjectDirectory = rootdir + "/" + directory + "/" + projectDir
		print "Project '", projectDir, "' is in ", fullProjectDirectory

		linkName = projectDir 
		if not os.path.islink(linkName):
			target = fullProjectDirectory
			os.symlink(target, linkName)
		else:
			print "Link to ", linkName, "exists already"
