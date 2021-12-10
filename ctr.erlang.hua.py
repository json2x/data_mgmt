#!/usr/bin/env /home/jcm/env/data_management/bin/python

import os, glob, sys, re, time, shutil
from datetime import datetime, timedelta

from xml.dom import minidom
import xml.etree.ElementTree as ET

SCRIPT_DIR = '/home/jcm/projects/DataMgmt'

#---------------------------
def main():
	print('')
	print('-- HUA ERLANG STATS VERIFICATION ---')
	
	xmlFile = interactor('Input XML file path')
	if os.path.isfile(xmlFile):
		#xmldoc = minidom.parse('{}/Dumps/A20200728.0500+0800-0600+0800_MS01DLUC.xml'.format(SCRIPT_DIR))
		xmldoc = minidom.parse(xmlFile)
		measInfos = xmldoc.getElementsByTagName('measInfo')
		
		if len(measInfos) > 0:
			print("Searching XML for measInfo with \n[measInfoId 83888114 with meastypes 84163237] and [measInfoId 83888115 with meastypes 84163338]")
			print('')
			for measInfo in measInfos:
				#Check for measInfo 83888114 & 83888115
				if measInfo.hasAttribute('measInfoId') and (measInfo.getAttribute('measInfoId') == '83888114' or measInfo.getAttribute('measInfoId') == '83888115'):
					print('---------------')
					print('measInfoId: {}'.format(measInfo.getAttribute('measInfoId')))
					
					#check for measTypes 84163237 & 84163338 respectively
					measTypes = measInfo.getElementsByTagName('measTypes')
					#print('Count of measTypes Node: {}'.format(len(measTypes)))
					
					#expecting one measTypes node in each measInfo node
					measTypesValues = measTypes[0].firstChild.nodeValue
					measTypesList = measTypesValues.split(' ')
					counterIndex = 0
					if measInfo.getAttribute('measInfoId') == '83888114':
						print("measType: 84163237")
						if '84163237' in measTypesList:
							counterIndex = measTypesList.index('84163237')
							print('Counter index num: {}'.format(counterIndex))
							print('[Found!]')
						else:
							print('MISSING')
					elif measInfo.getAttribute('measInfoId') == '83888115':
						print("measTypes: 84163338")
						if '84163338' in measTypesList:
							counterIndex = measTypesList.index('84163338')
							print('Counter index num: {}'.format(counterIndex))
							print('[Found!]')
						else:
							print('MISSING')
					
					print('')
					for childNode in measInfo.childNodes:
						if childNode.nodeType == 1: #'ELEMENT_NODE'
							if childNode.tagName != 'measTypes':
								if childNode.tagName != 'measValue':
									attrStr = ' '.join(['{}={}'.format(attr[0],attr[1]) for attr in childNode.attributes.items()])
									print('{} {}'.format(childNode.tagName,attrStr))
					
					measValues = measInfo.getElementsByTagName('measValue')
					print('Count of measObjLdn: {}'.format(len(measValues)))
					for measValue in measValues:
						attrStr = ' '.join(['{}'.format(attr[1]) for attr in measValue.attributes.items()])
						measResults = measValue.getElementsByTagName('measResults')
						#expecting one measResults node in each measValue node
						measResultsStr = measResults[0].firstChild.nodeValue
						measResultsList = measResultsStr.split(' ')
						
						print("[{}]:\t{}".format(attrStr, measResultsList[counterIndex]))
							
							
					print('---------------')
					print('')
	else:
		print('Invalid file path.')
		print('Please check if file is in the correct path.')
	
	
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
