from functools import partial
import http.server as BaseHTTPServer
from ClientInterface import ClientInterface
from threading import Thread
import os
import shutil
import socket

class HTTPServer(ClientInterface):
    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
        def __init__(self, http_server, *kwargs):
            self._http_server = http_server
            super(HTTPServer.Handler, self).__init__(*kwargs)

        def do_GET(self):
            with open(self._http_server._path, 'rb') as f:
                self.send_response(200)
                self.send_header("Content-Type", 'application/octet-stream')
                self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(self._http_server._path)))
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)

            self._http_server._is_running = False
    
    @staticmethod
    def _get_ip():
        return socket.gethostbyname(socket.gethostname())
    
    def __init__(self, ip='', port=9595, protocol_version="HTTP/1.0", password='', timeout=120):
        self._ip = ip if ip else HTTPServer._get_ip()
        self._port = port
        self._protocol_version = protocol_version
        self._thread = None
        self._http = None
        self._timeout = timeout
        self._is_running = True
        
    def shutdown(self):
        self._is_running = False
        if self._thread:
            self._thread.join()
    
    def __del__(self):
        self.shutdown()
        
    @staticmethod
    def validate_init_params(self, params):
        # raise error on bad params. Return nothing
        pass
    
    @staticmethod
    def _serve_forever(http):
        while http._is_running:
            http._http.handle_request()
        
    def upload(self, local_file_path):
        self._path = local_file_path
        self._is_running = True
        handle_class = partial(HTTPServer.Handler, self)
        handle_class.protocol_version = self._protocol_version
        self._http = BaseHTTPServer.HTTPServer((self._ip, self._port), handle_class)
        self._thread = Thread(target=HTTPServer._serve_forever, args=(self,))
        self._thread.start()
        return socket.gethostbyname(socket.gethostname()) + ":" + str(self._port)