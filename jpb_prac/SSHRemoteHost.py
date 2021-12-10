import paramiko
import scp
import sys

class SSHRemoteHost:
	creds = {}
	client = {}
	session = False
	conStatus = False
	
	#--------------------------------
	def __init__(self, remote_host_creds = {}):
		if remote_host_creds:
			self.creds = remote_host_creds
		else:
			raise Exception('Please provide remote host credentials.')
			
	#--------------------------------
	def connect(self):
		""" SSH connect to remote host. """
		try:
			self.client = paramiko.SSHClient()
			self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

			my_rsa_key = paramiko.RSAKey.from_private_key_file(self.creds['rsa_key'])
			self.session = self.client.connect(self.creds['host'], username=self.creds['user'], password=self.creds['pwd'], port=self.creds['port'], pkey=my_rsa_key)
			self.conStatus = True
			print("\nSession: {}\nConn Status: {}".format(self.session, self.conStatus), flush=True)

		except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException) as Err:
			print(Err)

		except:
			self.disconnect()
			print("Connection failed.")
			print("Unexpected error:")
			print(sys.exc_info())
			
	#--------------------------------
	def disconnect(self):
		"""
		Disconnect from the ssh client. If this fails, for instance
		if the connection instance doesn't exist, ignore the exception.
		"""
		try:
			self.conStatus = False
			self.client.close()
		except:
			pass
			
	#--------------------------------
	def execute(self, command):
		"""
		Execute remote host command
		"""
		strOut = ''
		strErr = ''
		try:
			if self.conStatus:
				(stdin, stdout, stderr) = self.client.exec_command(command)
				strErr = stderr.read().decode('utf-8')
				strOut = stdout.read().decode('utf-8')
				
				if strErr:
					print(strErr)
					print(strOut)
				else:
					print(strOut)
			
		except paramiko.SSHException as err:
			print(Err)
		except:
			self.disconnect()
			print("Unexpected error:")
			print(sys.exc_info())
		
		return {"Output": strOut, "Error": strErr}
		
	#--------------------------------
	def get_remote_file(self, remote_filepath, local_filepath):
		try:
			if self.conStatus:
				print("Copying {}\nto {}... ".format(remote_filepath, local_filepath), end='', flush=True)
				myScp = scp.SCPClient(self.client.get_transport())
				myScp.get(remote_filepath, local_filepath)
				myScp.close()
				print("[OK]")
		except scp.SCPException as Err:
			print(Err)
		except:
			self.disconnect()
			print("Unexpected error:")
			print(sys.exc_info())

	#--------------------------------
	def put_remote_file(self, local_filepath, remote_filepath):
		try:
			if self.conStatus:
				print("Copying {}\nto {}... ".format(local_filepath, remote_filepath), end='', flush=True)
				myScp = scp.SCPClient(self.client.get_transport())
				myScp.put(local_filepath, remote_filepath)
				myScp.close()
				print("[OK]")
		except scp.SCPException as Err:
			print(Err)
		except:
			self.disconnect()
			print("Unexpected error:")
			print(sys.exc_info())