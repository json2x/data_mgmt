#!/usr/bin/env /home/jcm/env/data_management/bin/python

import os, glob, sys, re, time, shutil
from datetime import datetime, timedelta
import subprocess
import csv

from xml.dom import minidom
import xml.etree.ElementTree as ET

SCRIPT_DIR = '/home/jcm/projects/DataMgmt'
#OUTPUT_DIR = 'OutputFiles'
OUTPUT_DIR = '/home/jcm/mnt/DM_ADHOC_TEAM/DATA_CHECKING'
#---------------------------
def main():
	print('')
	print('-- HUA COUNTER CHECKER ---')
	
	xmlzipFilePath = interactor('Input HUA raw data file path')
	if os.path.isfile(xmlzipFilePath):
		measInfoId = interactor('Input measInfoId')
		measType = interactor('Input measType')
		findCounter(xmlzipFilePath, measInfoId, measType)
	else:
		print('Invalid directory path.')
		print('Please check if directory is in the correct path.')
	
#---------------------------
def findCounter(xmlFile, measInfoId, measType):
	foundMeasInfoID = False
	foundMeasType = False
	xmldoc = minidom.parse(xmlFile)
	measInfosDOM = xmldoc.getElementsByTagName('measInfo')
	
	if len(measInfosDOM) > 0:
		for measInfoDOM in measInfosDOM:
			#Check for measInfo tag and measInfoId attribute
			if measInfoDOM.hasAttribute('measInfoId') and (measInfoDOM.getAttribute('measInfoId') == measInfoId):
				foundMeasInfoID = True
				print('---------------')
				print('measInfoId: {}'.format(measInfoDOM.getAttribute('measInfoId')))
				
				measTypesDOM = measInfoDOM.getElementsByTagName('measTypes')
				measTypesValues = measTypesDOM[0].firstChild.nodeValue
				measTypesList = measTypesValues.split(' ')
				counterIndex = 0
				if measType in measTypesList:
					foundMeasType = True
					print('measType: {}'.format(measType))
					counterIndex = measTypesList.index(measType)
					
					try:
						outputFileName = '{}/Hua_Counter_{}_{}_{}.csv'.format(OUTPUT_DIR, time.strftime("%Y%m%d.%H%M%S"), measInfoId, measType)
						with open(outputFileName, 'w', newline='') as outputFile:
							writer = csv.writer(outputFile)
							
							statDict = {}
							measValuesDOM = measInfoDOM.getElementsByTagName('measValue')
							for measValueDOM in measValuesDOM:
								#attr[0]  attr[1]
								#attrName="AttrValue"
								attrStr = ' '.join(['{}'.format(attr[1]) for attr in measValueDOM.attributes.items()])
								measResults = measValueDOM.getElementsByTagName('measResults')
								#expecting one measResults node in each measValue node
								measResultsStr = measResults[0].firstChild.nodeValue
								measResultsList = measResultsStr.split(' ')
								measResultValue = measResultsList[counterIndex]
								
								#prepAttrStringForSplitting
								attrStr = attrStr.replace(':', ',')
								print('{},{}'.format(attrStr, measResultValue))
								csvRowStr = '{},{}'.format(attrStr, measResultValue)
								writer.writerow(csvRowStr.split(','))
								#statDict[attrStr] = measResultValue
								#print(statDict)
						
						print('')
						print('---------------')
						print('Output file saved in:')
						print(outputFileName.replace('/home/jcm/mnt', '\\\\10.150.20.104\\tcm').replace('/', '\\'))
					except OSError as e:
						print('{}: {}'.format(e.errno, e.strerror))
						print(e.filename)
					except FileExistsError:
						print('File already exist!')
						exc_type, exc_obj, exc_tb = sys.exc_info()
						fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
						print("{}: {}".format(exc_type, exc_obj))
						print(fname)
					except:
						exc_type, exc_obj, exc_tb = sys.exc_info()
						fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
						print("{}: {}".format(exc_type, exc_obj))
						print(fname)
					
		if foundMeasInfoID == False:
			print('<measTypes> * {} * </measTypes> NOT FOUND'.format(measType))
		else:
			if foundMeasType == False:
				print('<measInfo measInfoId="{}"> NOT FOUND'.format(measInfoId))
				
		print('---------------')
		print('')
	
	
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
