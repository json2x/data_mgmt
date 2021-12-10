import paramiko
import scp

class SSHRemoteHost:
	creds = {}
	client = {}
	session = False
	conStatus = False
	
	#-------------------------------------
	def __init__(self, remote_host_creds = {}):
		if remote_host_creds:
			creds = remote_host_creds
		else:
			raise Exception('Please provide remote host credentials.')
		
	#--------------------------------
    def connect():
        """ SSH connect to remote host. """
        try:
			slef.client = paramiko.SSHClient()
			slef.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			
			my_rsa_key = paramiko.RSAKey.from_private_key_file(creds['rsa_key'])
			self.session = slef.client.connect(creds['host'], username=creds['user'], password=creds['pwd'], port=creds['port'], pkey=my_rsa_key)
			self.conStatus = True
			
		except (AuthenticationException, BadHostKeyException, SSHException, socket.error) as Err:
			print(Err)
			
		except:
			self.disconnect()
			print("Unexpected error:", sys.exc_info()[0])
		
	#--------------------------------
    def disconnect(self):
        """
        Disconnect from the ssh client. If this fails, for instance
        if the connection instance doesn't exist, ignore the exception.
        """
        try:
			self.conStatus = False
            slef.client.close()
        except:
            pass

	#--------------------------------
    def execute(self, command):
        """
        Execute remote host command
        """
        try:
            if self.connection:
                (stdin, stdout, stderr) = slef.client.exec_command(command)
        except SSHException as err:
            print(Err)
		except:
			self.disconnect()
			
	#--------------------------------
    def get_remote_file(self, remote_filepath, local_filepath):
		try:
			scp = scp.SCPClient(self.client.get_transport())
			scp.get(remote_filepath, local_filepath)
			scp.close()
		except SCPException as Err:
			print(Err)
		except:
			self.disconnect()
		
	#--------------------------------
    def put_remote_file(self, local_filepath, remote_filepath):
		try:
			scp = scp.SCPClient(self.client.get_transport())
			scp.put(local_filepath, remote_filepath)
			scp.close()
		except SCPException as Err:
			print(Err)
		except:
			self.disconnect()