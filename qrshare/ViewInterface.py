class ViewInterface(object):
    def __init__(self, *args):
        super(ViewInterface, self).__init__(*args)

    @staticmethod
    def validate_init_params(**params):
        pass

    def view(self, str):
        raise NotImplementedError()
