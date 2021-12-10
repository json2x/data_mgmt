#!/usr/bin/env /home/jcm/env/data_management/bin/python

import os, glob, sys, re, time, shutil
from datetime import datetime, timedelta
from oracle import Oracle
import csv

pmserver = ""

OUTPUT_DIR = '/home/jcm/mnt/DM_ADHOC_TEAM/DATA_CHECKING'
#---------------------------
def main():
	print('What PM database server')
	print('1: MBB Checking')
	print('2: FBB Checking')
	server = input('\nSelect PM server: ')

	if server == '1':
		#goes to MBB Database (10.150.6.34)
		SERVER_CREDS = {
			"pmdb": {"host": "10.150.6.34", "user": "pm4h_ad", "pwd": "ACROSS_ad_2013", "port": "1522", "db": "acrosspm",},}
		pmserver = "MBB Checking"
		queryResmodelTableNumber(SERVER_CREDS, pmserver)

	elif server == '2':
		#goes to FBB Database (10.150.6.120)
		SERVER_CREDS = {
			"pmdb": {"host": "10.150.6.120", "user": "pm4h_ad", "pwd": "ACROSS_ad_2013", "port": "1522", "db": "acrosspm",},}
		pmserver = "FBB Checking"
		queryResmodelTableNumber(SERVER_CREDS, pmserver)
	else:
		print('\nInvalid Input')

#---------------------------
def queryResmodelTableNumber(SERVER_CREDS, pmserver):
	queryDict = {}
	objNum = ''
	oracle = Oracle()
	print('Connecting to USA Oracle DB...', end="", flush=True)
	oracle.connect(SERVER_CREDS['pmdb']['user'], SERVER_CREDS['pmdb']['pwd'], SERVER_CREDS['pmdb']['host'], SERVER_CREDS['pmdb']['port'], SERVER_CREDS['pmdb']['db'])
	if oracle.connection:
		print('[OK]')
		print('')
		print("======================================")
		print("         '{}'".format(pmserver))
		print("======================================")
		modelname = input('Input resmodel name: ')
		print("Checking resmodel table number...")
		queryDict['resmodel'] = "select tablename from pm4h_mo.mdl_resmodeltable t where t.modelid in (select \
		modelid from pm4h_mo.mdl_resmodel s where s.modelname = '{}')".format(modelname)
		print("--------------------------------------")
		print("          Query to execute            ")
		print("--------------------------------------")
		print("select tablename \n  from pm4h_mo.mdl_resmodeltable t \nwhere t.modelid in \n  (\n \
		select modelid \n    from pm4h_mo.mdl_resmodel s \n    where s.modelname = '{}'\n  );".format(modelname))
		print("------------------------------")
		oracle.execute(queryDict['resmodel'])

		result = oracle.cursor.fetchall()
		print("\n\n")
		print("======================================")
		print("              Query Result")
		print("--------------------------------------")
		print("Count of result: {}".format(len(result)))
		for row in result:
			print(row)
			objNum = row[0]
		print("==============================")

		if objNum:
			print("\n")
			print("Checking EMSENTITYNAME/ID...")
			queryDict['emsentityname'] = "select a.hostname, b.objname, t.EMSENTITYID, t.EMSENTITYNAME \
			from pm4h_ad.eam_emsentity t, pm4h_ad.eam_eamhost a, pm4h_mo.obj_{} b \
			where t.eamserverid = a.serverid and t.emsentityid = b.emsentityid".format(objNum)
		print("------------------------------------------------------------------------------------------")
		print("                                      Query to execute")
		print("------------------------------------------------------------------------------------------")
		print("select a.hostname, b.objname, t.EMSENTITYID, t.EMSENTITYNAME \n \
		from pm4h_ad.eam_emsentity t, pm4h_ad.eam_eamhost a, pm4h_mo.obj_{} b \n \
		where t.eamserverid = a.serverid and t.emsentityid = b.emsentityid;".format(objNum))
		print("------------------------------------------------------------------------------------------")
		print('Please wait for awhile...', end="", flush=True)
		oracle.execute(queryDict['emsentityname'])

		result = oracle.cursor.fetchall()
		print("[DONE]\n")
		print("Count of Result: {}".format(len(result)))
		outputFileName = '{}/{}_{}.csv'.format(OUTPUT_DIR, modelname, time.strftime("%Y%m%d.%H%M%S"))
		with open(outputFileName, 'w', newline='') as outputFile:
			writer = csv.writer(outputFile)
			writer.writerow(['pmeam', 'Network Element', 'EMSENTITYID', 'EMSENTITYNAME'])
			for row in result:
				writer.writerow(row)

		print("File name is: {}_{}.csv".format(modelname, time.strftime("%Y%m%d.%H%M%S")))
		print("\nOutput file saved in\nLinux: {}".format(OUTPUT_DIR))
		print("Windows: \\\\10.150.20.104\DM_ADHOC_TEAM\DATA_CHECKING")
		print("\n")
		oracle.disconnect()
	else:
		print('[Failed]')

#---------------------------
if __name__ == "__main__":
	os.system('clear')
	starTime = datetime.now()
	print("\nRun Datetime: {}".format(starTime))
	print("--------------------------------------")
	print("    Data Management Slave IP Parse    ")
	print("--------------------------------------")

	main()

	endTime = datetime.now()
	deltaDt = endTime - starTime
	print(deltaDt)
	print("<<<<< End of Script >>>>>")
