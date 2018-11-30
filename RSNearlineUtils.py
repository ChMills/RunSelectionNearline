import sys
import os

### Log file

def log(logFile, msg, verbose=False):
	if verbose:
		print msg
	logFile.write(msg + "\n")
	return