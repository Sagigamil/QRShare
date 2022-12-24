"""
This file defines the HTTPServer class, which is a concrete implementation of the ClientInterface class.

The HTTPServer class implements a simple HTTP server that listens for client requests on a specified IP address and port. It has a single method, 'upload', which takes a local file path as input and serves the file to clients over HTTP.
"""

import os
import shutil
import socket
import ipaddress

from functools import partial
import http.server as BaseHTTPServer
from .ClientInterface import ClientInterface
from threading import Thread


class HTTPServer(ClientInterface):
    """
    A concrete implementation of the ClientInterface class that serves files over HTTP using a simple HTTP server.
    """
    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
        """
        A request handler for the HTTP server that serves a single file to clients.
        """
        def __init__(self, http_server, *kwargs):
            """
            Initializes the request handler instance.

            Args:
                http_server (HTTPServer): The HTTP server instance.
                *kwargs: Additional arguments.
            """
            self._http_server = http_server
            super(HTTPServer.Handler, self).__init__(*kwargs)

        def do_GET(self):
            """
            Handles GET requests from clients.

            Returns:
                None
            """
            with open(self._http_server._path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header(
                    "Content-Disposition",
                    'attachment; filename="{}"'.format(
                        os.path.basename(self._http_server._path)
                    ),
                )
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)

            self._http_server._is_running = False

    @staticmethod
    def _get_ip():
        """
        Gets the local IP address of the host.

        Returns:
            str: The local IP address of the host.
        """
        return socket.gethostbyname(socket.gethostname())


    def __init__(self, ip="", port=9595):
        """
        Initializes the HTTPServer object.

        Args:
            ip (str, optional): The IP address to bind the HTTP server to. Defaults to the local IP address of the host.
            port (int, optional): The port to bind the HTTP server to. Defaults to 9595.
        
        Attributes:
            _ip (str): The IP address to bind the HTTP server to.
            _port (int): The port to bind the HTTP server to.
            _protocol_version (str): The protocol version to use for the HTTP server.
            _thread (Thread): The thread object used to run the HTTP server.
            _http (BaseHTTPServer.HTTPServer): The HTTP server object.
            _is_running (bool): A flag indicating whether the HTTP server is currently running.
        """
        self._ip = ip if ip else HTTPServer._get_ip()
        self._port = port
        self._protocol_version = "HTTP/1.0"
        self._thread = None
        self._http = None
        self._is_running = True

    def shutdown(self):
        """
        Shutdowns the HTTP server.

        This method sets the `_is_running` variable to `False`, which causes the server to stop handling requests.
        If a `_thread` is running, it will be joined to the main thread.
        """
        self._is_running = False
        if self._thread:
            self._thread.join()

    @staticmethod
    def validate_init_params(**params):
        """
        Validates the parameters passed to the constructor of the HTTPServer class.

        This method checks if the `ip` and `port` fields are present in the `params` dictionary and if their values are of the correct type (string for `ip` and integer for `port`). It also checks if the `ip` is a valid IP address and if the `port` is within the valid range (1-65535). If any of these checks fail, an exception is raised.

        Args:
            params (dict): A dictionary of parameters passed to the constructor of the HTTPServer class.

        Raises:
            Exception: If the `ip` or `port` fields are missing from the `params` dictionary, or if their values are of the incorrect type, or if the `ip` is an invalid IP address, or if the `port` is outside the valid range (1-65535).
        """
        if 'ip' not in params.keys():
            raise Exception('params has no field \'ip\'')
        
        if not isinstance(params['ip'], str):
            raise Exception('param \'ip\' has to be a string')
        
        if 'port' not in params.keys():
            raise Exception('params has no field \'ip\'')
        
        if not isinstance(params['port'], int):
            raise Exception('param \'port\' has to be an int')
        
        # check if the ip is a valid ip address:
        ipaddress.ip_address(params['ip'])
        
        # check if the port is a valid port:
        if params['port'] < 1 or params['port'] > 65535:
            raise Exception('param \'port\' is invalid')  
        
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
