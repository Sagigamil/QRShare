import qrcode
from .ViewInterface import ViewInterface


class QRView(ViewInterface):
    def __init__(self, *args):
        # TODO
        pass

    @staticmethod
    def validate_init_params(self, params):
        # TODO
        pass

    def view(self, str):
        img = qrcode.make(str)
        img.show()
