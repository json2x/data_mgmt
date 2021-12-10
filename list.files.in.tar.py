#!/usr/bin/env /home/jcm/env/generic/bin/python

import os, glob, sys, re, time, shutil
from datetime import datetime, timedelta
import subprocess


SCRIPT_DIR = '/home/jcm/projects/DataMgmt'

#---------------------------
def main():
	
	tar_file = interactor('Input .tar file path')
	
	print(tar_file)
	
#---------------------------
def interactor(question, choices = {}, returnKey = False):
	return_value = False
	if choices:
		print("{}: ".format(question))
		for choice, choice_text in choices.items():
			print("{}.) {}".format(choice, choice_text))
		
		selection = input("Input choice: ")
		if not selection.isdigit():
			if returnKey:
				return_value = selection
			elif selection.upper() in choices.keys():
				return_value = choices[selection.upper()]
			elif selection.lower() in choices.keys():
				return_value = choices[selection.lower()]
			else:
				print("Invalid choice")
		else:
			if returnKey:
				return_value = selection
			elif selection in choices.keys():
				return_value = choices[selection]
			else:
				print("Invalid choice")
	else:
		return_value = input("{}: ".format(question))
		
	return return_value
	
#---------------------------	
if __name__ == "__main__":
	starTime = datetime.now()
	print("\nRun Datetime: {}".format(starTime))
	print("--------------------------------------")
	print("    Data Management Data Checking     ")
	print("--------------------------------------")
	
	main()
	
	endTime = datetime.now()
	deltaDt = endTime - starTime
	print(deltaDt)
	print("<<<<< End of Script >>>>>")
