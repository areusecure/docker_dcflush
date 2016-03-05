import os
import json
from datetime import datetime
from shutil import rmtree

NAME = "Docker(R) dead container directories flush utility"

LICENSE = """
The MIT License (MIT)
Copyright (c) 2016 Areusecure AB

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


# Some standard exit codes
errors = {0:'Success',1:'General error',2:'Mis-use of bash shell builtins',126:'Command could not execute',\
	127:'Command not found', 128:'Invalid argument to exit()',130:'Terminated by Control-C',137:'Error signal 9 (kill -9 PID)'}

# Directory containing docker containers and their .json-files to be parsed
dir = "/var/lib/docker/containers"

# Number of warnings due to running containers (we skip deleting running containers)
warnings = 0

# Get time difference between start and finish in minutes and seconds, sometimes the date-time reference is off in the json-files, hence the clumpsy try-clause
def get_uptime(t1,t2,format="%Y-%m-%dT%H:%M:%S.%f"):
	try:
		if len(t1) > 26:
			started = datetime.strptime(t1[:-4],format)
		if len(t2) > 26:
			ended = datetime.strptime(t2[:-4],format)
		else:
			started = datetime.strptime(t1,format)
			ended = datetime.strptime(t2,format)
	
		difference = ended-started
		seconds = int(round(difference.seconds))
		minutes = seconds / 60
		seconds_diff = seconds - (minutes * 60)
	except:
		minutes="[unknown]"
		seconds_diff="[unknown]"
	return minutes, seconds_diff
	
def get_error(errorcode):
	if int(errorcode) in errors.keys():
		return errors[errorcode]
	else:
		return "Unknown error"

def get_exposed_ports(ports):
	if type(ports) is dict:
		return u','.join(k for k in ports.keys())
	if type(ports) is str:
		return ports

def get_dir_contents(directory):
	return [path for path in os.listdir(directory)]

# parse list of directories, open and load config.v2.json-file, print properties and prompt for deletion. 
def get_props(configpaths):
	logbuffer = ""
	delete_all_stopped = False
	count = 1
	deleted_dirs = 0
	# run through each dir in the list of dirs
	for v2config in configpaths:
		# open and load the config-file
		with open((v2config + "/config.v2.json"),"r") as f:
			configdata = json.loads(f.read())
			uptime = get_uptime(configdata["State"]["StartedAt"],configdata["State"]["FinishedAt"])
			logdata = "{}. Started: {}\nName: {}\nImage: {}\nRunning: {}\nExit code: {} ({})\nManually stopped: {}\nExposed ports: {}\nUptime: {} minutes and {} seconds\n".format(str(count),configdata["State"]["StartedAt"],\
			configdata["Name"].strip("/"),configdata["Config"]["Image"],configdata["State"]["Running"],configdata["State"]["ExitCode"], \
			get_error(configdata["State"]["ExitCode"]),configdata["HasBeenManuallyStopped"], \
			get_exposed_ports(configdata.get("Config").get("ExposedPorts","")),uptime[0], uptime[1])
			print logdata
			logbuffer += logdata
			count += 1
			# Run through our routine only if the container is marked as not running.
			if configdata["State"]["Running"] == False:
				if delete_all_stopped == False:
					accept = raw_input("You are about to Remove \"{0}\" ({1}), are you sure you want to remove {0}? (y)es/(n)o/(a)ll)".format(configdata["Name"].strip("/"),v2config))
			
				if accept.lower() == 'y' or accept.lower() == 'a' or delete_all_stopped == True:
					logdata = "Removing {0}\nDirectory: {1}\n\n".format(configdata["Name"].strip("/"),v2config)
					print logdata
					logbuffer += logdata
					if accept.lower() == 'a':
						delete_all_stopped = True
					rmtree(v2config)	
					deleted_dirs +=1
				else:
					logdata = "Canceled removal of {0}\n\n".format(configdata["Name"].strip("/"))
					print logdata
					logbuffer += logdata
			
			else:
				logdata = "Warning! Will not remove running containers, please stop them before removing their directories!\n\n"
				print logdata
				logbuffer += logdata
				warnings +=1
			print "\n\n"
	logdata = "{} container-directories were removed.".format(deleted_dirs)
	print logdata
	logbuffer += logdata
	with open("./docker_dcflush.log","w") as f:
		f.write(logbuffer)

def main():
	print "Docker dead container flush utility\n"
	print LICENSE
	license_response = raw_input("\n\nDo you accept the license stated above? (yes/no)")
	if license_response == 'yes':
	
		# get contents of directory specified in variable 'dir'
		top_dir_contents = get_dir_contents(dir)
		# add full directory paths to a list
		files = [(dir + "/" + directory) for directory in top_dir_contents]
		# process the list
		get_props(files)
	
		if warnings > 0:
			print "Warnings were generated (trying to delete running containers), no running containers were removed - please review output"
	
		print "Docker dead-container flush has finished."
		print "Author: Jonathan James <jj@areusecure.se>"
	else:
		print "Quitting."
		exit(0)

if __name__ == '__main__':
	main()
