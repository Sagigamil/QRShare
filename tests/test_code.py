from src.FTPClient import FTPClient
from src.QRView import QRView

LOCAL_FILE_PATH = 'dummy_file.txt'

def main():
    with open(LOCAL_FILE_PATH, 'w') as f:
        f.write('This is an amazing file')
    
    client = FTPClient('localhost', 69, 'user', '12345678')
    view = QRView()
    
    remote_path = client.upload(LOCAL_FILE_PATH)
    view.show(remote_path)
    