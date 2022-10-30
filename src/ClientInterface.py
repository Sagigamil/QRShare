
class ClientInterface(object):
    def __init__(self, *args):
        super(ClientInterface, self).__init__(*args)
        
    def upload(self, local_file_path):
        raise NotImplementedError()
    
    @staticmethod
    def validate_init_params(self, params):
        raise NotImplementedError()
