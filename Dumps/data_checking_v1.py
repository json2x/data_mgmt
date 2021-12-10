#!/usr/bin/env /home/jcm/env/data_management/bin/python

import subprocess
import os, glob, sys, re, time, shutil
from datetime import datetime, timedelta
from oracle import Oracle
from SSHRemoteHost import SSHRemoteHost

SCRIPT_DIR = '/home/jcm/projects/DataMgmt'
PRIVATE_RSA_KEY = "{}/private.ppk".format(SCRIPT_DIR)
PATH_EMS_PARSE_BACKUP = "/netwatcher/spool/emsperformance/{}/{}/parse_backup"
SERVER_CREDS = {
	"pmdb": {"host": "10.150.6.36", "user": "pm4h_ad", "pwd": "ACROSS_ad_2013", "port": "1522", "db": "acrosspm",},
	"pmeam01": {"host": "10.150.6.42", "user": "acrosspm", "pwd": "Huawei@12345", "port": "22", "rsa_key": PRIVATE_RSA_KEY},
	"pmeam02": {"host": "10.150.6.43", "user": "acrosspm", "pwd": "Huawei@12345", "port": "22", "rsa_key": PRIVATE_RSA_KEY},
	"pmeam03": {"host": "10.150.6.45", "user": "acrosspm", "pwd": "Huawei@12345", "port": "22", "rsa_key": PRIVATE_RSA_KEY},
	"pmeam04": {"host": "10.150.6.61", "user": "acrosspm", "pwd": "Huawei@12345", "port": "22", "rsa_key": PRIVATE_RSA_KEY},
	"pmeam05": {"host": "10.150.6.80", "user": "acrosspm", "pwd": "Huawei@12345", "port": "22", "rsa_key": PRIVATE_RSA_KEY},
}
#---------------------------
def main():
	#Expected Output: {'Name': server[0], 'EMSEntityID': server[1], 'DirectoryName': server[3]}
	server = queryServerDetailsInUSAOracleDB()
	
	#Get remote raw data files and store in local directory.
	remoteRawDataFileDir = getRemoteRawDataFiles(server)
	#remoteRawDataFileDir = '/home/jcm/projects/DataMgmt/RawData/202007071554_44'
	
	boolYN = interactor('Searcing for a raw data of a certain device? (Y/N)')
	if boolYN == 'Y' or boolYN == 'y':
		zipfiles = {}
		devicename = interactor('Input raw data device name')
		device_raw_data_files = glob.glob('{}/*{}*.zip'.format(remoteRawDataFileDir, devicename))
		print("Found {} files for {}.".format(len(device_raw_data_files), devicename))
		
		ctr = 1
		if len(device_raw_data_files) > 0:
			for file in device_raw_data_files:
				#print("{}) {}\n".format(ctr, file))
				zipfiles[str(ctr)] = file
				ctr += 1
		
		print("\n======================================")
		zipfile = interactor('Select file to unzip', zipfiles)
		print("======================================")
		
		print('Unpacking zip file [{}]...'.format(zipfile), end='', flush=True)
		shutil.unpack_archive(zipfile, remoteRawDataFileDir)
		print('[OK]')
		
		print("\nResult file(s):")
		print("======================================")
		for file in glob.glob('{}/*.xml'.format(remoteRawDataFileDir)):
			print(file)
		print("======================================")
			
	elif boolYN == 'N' or boolYN == 'n':
		print('Nothing to do.')
	else:
		print('Invalid input.')
	
	
	#Search for device raw data file in the local directory containing the raw data files.

#---------------------------
def getRemoteRawDataFiles(server):
	remoteRawDataFileDir = ''
	print('Connecting to remote host {}...'.format(server['Name']), end="", flush=True)
	remoteHost = SSHRemoteHost(SERVER_CREDS[server['Name']])
	remoteHost.connect()
	if remoteHost.conStatus:
		print('[OK]')
		remote_path = PATH_EMS_PARSE_BACKUP.format(server['DirectoryName'], server['EMSEntityID'])
		datefilename = fileNameDate()
		#remoteHost.execute('cd {}; pwd'.format(remote_path))
		client_pipe = remoteHost.execute('cd {}; ls {}'.format(remote_path, datefilename))
		#client_pipe = remoteHost.execute('ls {}/{}'.format(remote_path, datefilename))
		remote_files = []
		if not client_pipe['Error']:
			remote_files = client_pipe['Output'].splitlines()
		
		boolYN = interactor('Would you like to process this files? (Y/N)')
		if boolYN == 'Y' or boolYN == 'y' and remote_files:
			''' Create separate dir for these raw data files '''
			strDateDir = datetime.now().strftime('%Y%m%d%H%M_%S')
			dirFullPath = '{}/RawData/{}'.format(SCRIPT_DIR, strDateDir)
			os.makedirs(dirFullPath)
			
			for remote_file in remote_files:
				local_fie_path = "{}/RawData/{}/{}".format(SCRIPT_DIR, strDateDir, remote_file)
				remote_file_path = "{}/{}".format(remote_path,remote_file)
				remoteHost.get_remote_file(remote_file_path, local_fie_path)
				print('Unpacking file...', end="", flush=True)
				shutil.unpack_archive(local_fie_path, "{}/RawData/{}".format(SCRIPT_DIR, strDateDir))
				print("[OK]")
				
			print("")
			print("=========================================================")
			print("Raw data files saved in local directory.")
			print("Path: {}/RawData/{}".format(SCRIPT_DIR, strDateDir))
			print("=========================================================")
			print("")
			remoteRawDataFileDir = "{}/RawData/{}".format(SCRIPT_DIR, strDateDir)
			
		elif boolYN == 'N' or boolYN == 'n':
			print('Script disconnect to remote host and end itself.')
		else:
			print('Invalid input.')
			print('Script disconnect to remote host and end itself.')
	
	remoteHost.disconnect()
	
	return remoteRawDataFileDir
	
#---------------------------
def fileNameDate():
	strDate = ''
	print('Specify raw data date/time')
	year = interactor('Input year (yyyy)')
	month = interactor('Input month (mm)')
	date = interactor('Input date (dd)')
	hour = interactor('Input hour (hh)')
	print('')
	return '{}{}{}{}*'.format(year, month, date, hour)
	
	
#---------------------------
def queryServerDetailsInUSAOracleDB():
	
	queryDict = {}
	serverDict = {}
	objNum = ''
	emsentityid = ''
	server = ''
	oracle = Oracle()
	print('Connecting to USA Oracle DB...', end="", flush=True)
	oracle.connect(SERVER_CREDS['pmdb']['user'], SERVER_CREDS['pmdb']['pwd'], SERVER_CREDS['pmdb']['host'], SERVER_CREDS['pmdb']['port'], SERVER_CREDS['pmdb']['db'])
	if oracle.connection:
		print('[OK]')
		print('')
		print("Checking resmodel table number...")
		modelname = interactor('Input resmodel name')
		queryDict['resmodel'] = "select tablename from pm4h_mo.mdl_resmodeltable t where t.modelid in (select \
		modelid from pm4h_mo.mdl_resmodel s where s.modelname = '{}')".format(modelname)
		print("------------------------------")
		print("Query to execute")
		print("------------------------------")
		print("select tablename \n  from pm4h_mo.mdl_resmodeltable t \nwhere t.modelid in \n  (\n    select modelid \n    from pm4h_mo.mdl_resmodel s \n    where s.modelname = '{}'\n  );".format(modelname))
		print("==============================")
		oracle.execute(queryDict['resmodel'])
		
		result = oracle.cursor.fetchall()
		print("")
		print("------------------------------")
		print("Query result")
		print("------------------------------")
		print("Count of result: {}".format(len(result)))
		for row in result:
			print(row)
			objNum = row[0]
		print("==============================")
		
		if objNum:
			print("")
			print("Checking EMSEntityID...")
			objname = interactor('Input object name')
			queryDict['emsentityid'] = "select emsentityid from pm4h_mo.obj_{} t where verendtime is null and objname = '{}'".format(objNum, objname)
			print("------------------------------")
			print("Query to execute")
			print("------------------------------")
			print("select emsentityid \n  from pm4h_mo.obj_{} t \n  where verendtime is null \n  and objname = '{}';".format(objNum, objname))
			print("==============================")
			oracle.execute(queryDict['emsentityid'])
			
			result = oracle.cursor.fetchall()
			print("")
			print("------------------------------")
			print("Query result")
			print("------------------------------")
			print("Count of result: {}".format(len(result)))
			for row in result:
				print(row)
				emsentityid = row[0]
			print("==============================")
			
		if emsentityid:
			print("")
			print("Checking Server of EMSEntityID: {}...".format(emsentityid))
			queryDict['usapm_server'] = "select a.hostname, t.* from pm4h_ad.eam_emsentity t, pm4h_ad.eam_eamhost a where t.eamserverid = a.serverid and t.emsentityid = '{}'".format(emsentityid)
			print("------------------------------")
			print("Query to execute")
			print("------------------------------")
			print("select a.hostname, t.* \n  from pm4h_ad.eam_emsentity t, pm4h_ad.eam_eamhost a t \n  where t.eamserverid = a.serverid and t.emsentityid = '{}';".format(emsentityid))
			print("==============================")
			oracle.execute(queryDict['usapm_server'])
			
			result = oracle.cursor.fetchall()
			print("")
			print("------------------------------")
			print("Query result")
			print("------------------------------")
			print("Count of result: {}".format(len(result)))
			for row in result:
				print(row)
				server = row
			print("==============================")
		
		if server:
			print("")
			serverDict = {'Name': server[0], 'EMSEntityID': server[1], 'DirectoryName': server[3]}
			print({'Name': server[0], 'EMSEntityID': server[1], 'DirectoryName': server[3]})
			print("")
			
		oracle.disconnect()
	else:
		print('[Failed]')
		
	return serverDict

#---------------------------
def interactor(question, choices = {}):
	return_value = False
	if choices:
		print("{}: ".format(question))
		for choice, choice_text in choices.items():
			print("{}.) {}".format(choice, choice_text))
		
		selection = input("Input choice: ")
		if not selection.isdigit():
			if selection.upper() in choices.keys():
				return_value = choices[selection.upper()]
			elif selection.lower() in choices.keys():
				return_value = choices[selection.lower()]
			else:
				print("Invalid choice")
		else:
			if selection in choices.keys():
				return_value = choices[selection]
			else:
				print("Invalid choice")
	else:
		return_value = input("{}: ".format(question))
		
	return return_value

#---------------------------	
def extract_all(archives, extract_path):
	for filename in archives:
		shutil.unpack_archive(filename, extract_path)
		
#---------------------------
def getLatestFile(filePath):
	try:
		list_of_files = glob.glob(filePath)
		latest_file = max(list_of_files, key=os.path.getctime)
	except:
		latest_file = 'No file'
		
	return latest_file
	
	
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
