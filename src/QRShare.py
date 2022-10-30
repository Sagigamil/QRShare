import sys

import FTPClient
import HTTPServer
import QRView

UPLOAD_PROTOCOLS = {
    'ftp' : FTPClient.FTPClient,
    'http_server' : HTTPServer.HTTPServer,
}

VIEWS = {
    'qr' : QRView.QRView,
}

def main():
    # TODO use argparse instead
    if len(sys.argv) <= 1:
        print("Please specify file to upload")
        return -1
    
    if len(sys.argv) != 2:
        print("Please provide one file only")
        return -1
    
    file_to_upload = sys.argv[-1]
    
    default_protocol = 'http_server'
    default_view = 'qr'
    
    client = UPLOAD_PROTOCOLS[default_protocol]()
    view = VIEWS[default_view]()
    
    path = client.upload(file_to_upload)
    view.view(path)
    

if __name__ == '__main__':
    main()