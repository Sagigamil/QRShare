from src.ClientInterface import ClientInterface

class FTPClient(ClientInterface):
    def __init__(self, ip, port, user='', password=''):
        # Build ftp object etc
        pass
    
    @staticmethod
    def validate_init_params(self, params):
        # raise error on bad params. Return nothing
        pass
    
    def upload(self, local_file_path):
        # implement ftp upload logic here. Return remote file path
        return "\\remote\\" + local_file_path