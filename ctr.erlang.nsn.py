#!/usr/bin/env /home/jcm/env/data_management/bin/python

import os, glob, sys, re, time, shutil
from datetime import datetime, timedelta
import subprocess

from xml.dom import minidom
import xml.etree.ElementTree as ET

SCRIPT_DIR = '/home/jcm/projects/DataMgmt'

NSN_MSC = {
	'MSC-998162', 'M101CMKT'
	'MSC-407678', 'M102CMKT'
	'MSC-407679', 'M103CMKT'
	'MSC-407681', 'M201CCLK'
	'MSC-407682', 'M202CCLK'
	'MSC-407683', 'M203CCLK'
	'MSC-359793', 'MS01AQCY'
	'MSC-359798', 'MS01B'
	'MSC-998273', 'MS02AQCY'
	'MSC-359795', 'MS02B'
	'MSC-390601', 'MS02TQCY'
	'MSC-998426', 'MS03A'
	'MSC-998427', 'MS03B'
	'MSC-998102', 'MS04A'
	'MSC-998148', 'MS04B'
	'MSC-998137', 'MS05B'
	'MSC-900845', 'MS06B'
	'MSC-406843', 'TR101MKT'
}
#---------------------------
def main():
	print('')
	print('-- NSN ERLANG STATS VERIFICATION ---')
	
	xmlzipFilePath = interactor('Input NSN MSC raw data file path')
	if os.path.isdir(xmlzipFilePath):
		#bashCommand = 'zgrep -i \'<measInfo measInfoId="TC">\' {}/*MSC*.xml.zip'.format(xmlzipFilePath)
		bashCommand = ['zgrep', '-i', "'<measInfo measInfoId=\"TC\">'", '{}/*MSC*.xml.zip'.format(xmlzipFilePath)]
		try:
			#zgrep = subprocess.run(bashCommand, stderr=subprocess.STDOUT, shell=True)
			zgrep = subprocess.run(bashCommand, capture_output=True, shell=True)
			print(zgrep)
			print(zgrep.CompletedProcess.output)
		except subprocess.CalledProcessError as e:
			print('Returned Non-zero return code.')
			print('Command: {}'.format(e.cmd))
			print('Return code: {}'.format(e.returncode))
			print("")
			print('Stdout: {}'.format(e.stdout))
			print("")
			print('Stderr: {}'.format(e.stderr))
	else:
		print('Invalid directory path.')
		print('Please check if directory is in the correct path.')
	
	
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
