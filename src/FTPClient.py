from xmlrpc.client import ProtocolError

from click import password_option
from ClientInterface import ClientInterface
from ftplib import FTP_PORT
import os

class FTPClient(ClientInterface):
    def __init__(        # Build ftp object etcself, ip, port, user='', password=''):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

        pass
    
    @staticmethod
    def validate_init_params(self, params):
        # raise error on bad params. Return nothing
        pass
    
    def upload(self, local_file_path):
        
        ftp = FTP(self.ip)
        ftp.login(user = self.user, passwd = self.password)
        ftp.cwd('/shared')
        filename = os.path.basename(local_file_path)
        file = open(local_file_path . 'rb')
        ftp.storbinary('STOR ' + filename , file)
        file.close()
        ftp.quit()

        return "ftp://" + self.user + ":" + self.password + "@" + self.ip + "/shared/" + filename