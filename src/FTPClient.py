from ftplib import FTP
import os
from src.ClientInterface import ClientInterface


class FTPClient(ClientInterface):
    def __init__(self, ip, port, user="", password="", remote_directory=""):
        self._ip = ip
        self._port = port
        self._user = user
        self._password = password
        self._remote_dir = remote_directory
        self._ftp = FTP(user=user, passwd=password)

    @staticmethod
    def validate_init_params(self, params):
        # raise error on bad params. Return nothing
        pass

    @staticmethod
    def _suggest_other_file_name(file_name, i):
        return f"({i}) {file_name}"

    def _is_file_already_exists(self, file_name):
        return file_name in self._ftp.nlst()

    def _get_valid_file_name(self, file_name):
        i = 0
        new_name = file_name
        while self._is_file_already_exists(new_name):
            new_name = self._suggest_other_file_name(file_name, i)
            i = i + 1

        return new_name

    def upload(self, local_file_path):
        file_name = os.path.basename(local_file_path)
        self._ftp.connect(host=self._ip, port=self._port)
        self._ftp.login(user=self._user, passwd=self._password)
        self._ftp.cwd(self._remote_dir)

        file_name = self._get_valid_file_name(file_name)
        with open(local_file_path, "rb") as file:
            self._ftp.storbinary(f"STOR {file_name}", file)

        self._ftp.close()

        full_path = os.path.join(self._remote_dir, file_name).replace("\\", "/")
        return (
            f"ftp://{self._user}:{self._password}@{self._ip}:{self._port}/{full_path}"
        )
