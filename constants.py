#!/usr/bin/env /home/jcm/env/data_management/bin/python

###### REMOTE DIRECTORY SETUP ######
EMSPERF_PATH = '/netwatcher/spool/emsperformance'
PARSEBACKUP_DIR = 'parse_backup'
EMSPERF_DIR = {
	'pmeam01': {
		'perfpath': EMSPERF_PATH,
		'perfdirs': {'1': 'AvaitProvisonV1', '2': 'HWM2000V2R3V2R12FISFTP', '3': 'SOLARWINDV1R2C20PLDT', 
			'4': 'HuaweiU2000TXN', '5': 'IONV1', '6': 'TEKELEC_SMSC', '7': 'ZTELTEV2R1'},
	},
	'pmeam02': {
		'perfpath': EMSPERF_PATH,
		'perfdirs': {'1': 'ERICSSON2GASNV1R2C20', '2': 'ERICSSON3G', '3': 'ERICSSON4G', '4': 'ERICSSON_ENM', 
			'5': 'ERICSSONGGSN', '6': 'ERICSSONSGSN', '7': 'NSNNETACTV1R2C20'}
	},
	'pmeam03': {
		'perfpath': EMSPERF_PATH,
		'perfdirs': {'1': 'CACTI', '2': 'HWITSV1R1C00SPC001', '3': 'CIENADFON', '4': 'HWU2000-Datacom', 
			'5': 'CommonEAMPackage', '6': 'HWU2000-Domestic', '7': 'ERICSSON3G', '8': 'HWU2000-MSAN+FTTH', 
			'9': 'HuaweiN2000-International', '10': 'UTStarcomNetman2020'}
	},
	'pmeam04': {
		'perfpath': EMSPERF_PATH,
		'perfdirs': {'1': 'AIRSPAN', '2': 'HWPIVOTeSight', '3': 'UTStarcomNetman2020', '4': 'HWM2000V2R3V2R12FISFTP', 
			'5': 'HWPIVOTU2000', '6': 'HWOneOCS'}
	},
	'pmeam05': {
		'perfpath': EMSPERF_PATH,
		'perfdirs': {}
	}
}
