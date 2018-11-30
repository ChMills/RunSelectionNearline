#!/usr/bin/env python

##############################################################################
### This code calls the run_selction.py script,
### performing run selection.
### Author: Charlie Mills
###			<Charlie.Mills@sussex.ac.uk>
### Adapted from DQHL client, written by Mark Stringer <m.stringer@qmul.ac.uk>

'''
TO ADD
Wait for dqhl, dqll to finish running
'''

### IMPORTS
import sys
import argparse
import os
import json
import datetime
import shutil
from subprocess import call
import rs_settings
from RSNearlineUtils import log
from rsdbtools import upload_data

sys.path.insert(0, ABSOLUTE_PATH_TO_RUN_SELECTION_CODE) ###CHANGE THIS - /home/nearline/runselection ???

from RUN_SELECTION_CODE import FUNCTIONS #need to format 

def runRSNearline(runNum, logFile, keepWorkingDir=False, verbose=False):
	log(logFile, "Performing Run Selection", verbose)

	#create and change to working directory

	rsNearlineDir = os.path.join(rs_settings.NEARLINE_RS_DIR)
	os.chdir(rsNearlineDir)
	workingDir = os.path.join(rsNearlineDir, "nearline_rs_%s" %runNum)
	if not os.path.isdir(workingDir):
		os.mkdir(workingDir)
	os.chdir(workingDir)

	log(logFile, "Running the run selection code...", verbose)

	###RUN RS SCRIPT HERE - currently a placeholder
	returnCode = FUNCTIONS() #EDIT THIS
	###RUN RS SCRIPT HERE - currently a placeholder

	if returnCode != 0:
		log(logFile, "The run selection script did not run correctly", verbose)
		logFile.close()
		sys.exit(2)

	rsfile = ""

	for fil in os.listdir(workingDir):
		if fil.endswith(".ratdb") and "RUNSELECTION" in fil and str(runNum) in fil: #this depends on output of runselection script
			rsfile = fil

	if rsfile == "":
		log(logFile, "No run selection table was produced", verbose)
		logFile.close()
		sys.exit(2)

	log(logFile, ("Uploading %s to Run Selection DB" %rsfile), verbose)
	try: #upload to rsbd
		table_name = 'runselection' #change this?
		with open(os.path.join(workingDir, rsfile), 'r') as data_file:
			table_data = json.load(data_file)
		if upload_data(table_name, args.runnumber, json.dumps(table_data)) == 0:
			log(
				logFile,
				"%s - rs():INFO: Upload to RSDB: OK\n" %(datetime.datetime.now().replace(microsecond = 0)),
				verbose
				)
		else:
			log(
				logFile,
				"%s - rs():INFO: Upload to RSDB: FALI\n" %(datetime.datetime.now().replace(microsecond = 0)),
				verbose
				)
			sys.exit(2)

	except Exception as e:
		log(
			logFile,
			"%s - rs():INFO: Upload to RSDB: Exception: %s\n" %(datetime.datetime.now().replace(microsecond = 0), e),
			verbose
			)

	#Remove working directory

	if not keepWorkingDir:
		log(logFile, "Cleaning up: removing run directory", verbose)
		shutil.rmtree(workingDir)

	log(logFile, "Run selection nearline tast complete", verbose)
	return


if __name__=="__main__":
	#Parse
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", dest="runnumber", help="Run number", type=int, required=True)
	parser.add_argument("-l", dest="logFile", help="Log file name", type=str, required=True)
	parser.add_argument("-t", dest="runtype", help="Run type", type=int)

	feature_parser = parser.add_mutually_exclusive_group(required=False)
	feature_parser.add_argument("--keepdir", dest="keepWorkingDir", help="Keep working directory (for debugging)", action='store_false')
	feature_parser.add_argument("--no-keepdir", dest="keepWorkingDir", help="Remove working directory when finished (default)", action='store_false')
	parser.set_defaults(keepWorkingDir=False)

	feature_parser = parser.add_mutually_exclusive_group(required=False)
	feature_parser.add_argument("--verbose", dest="verbose", help="Print log messages to screen (for debugging)", action='store_true')
	feature_parser.add_argument("--no-verbose", dest="verbose", help="Print log messages to file (default)", action='store_true')
	parser.set_defaults(verbose=False)

	args = parser.parse_args()

	#Open and initiate log file

	logFile = open(args.logFile, "a")
	logFile.write("Parsed arguments and writing to log file\n")
	logFile.write("		Run number: 		%d\n" %args.runnumber)
	logFile.write("		Log file: 			%s\n" %args.logFile)
	logFile.write("		Keep working dir? 	%s\n" %args.keepWorkingDir)
	logFile.write("		Verbose?			%s\n" %args.verbose)
	logFile.write("\n")

	if "RATROOT" not in os.environ: #is this needed? RAT is not being used, kept for additional error catching
		logFile.write("Error: RATROOT env variable not set")
		sys.exit(1)

	else:
		logFile.write("Using RAT: %s" %os.environ["RATROOT"])

	#Run the run selection code

	logFile.write("Running run selection nearline\n")
	runRSNearline(args.runnumber, logFile, args.keepWorkingDir, args.verbose)

	logFile.close()
	sys.exit(0)