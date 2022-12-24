import os
import sys
import json
import importlib

USER_CONFIG_JSON_NAME = 'qrshare_config.json'

default_json_file = {
    'protocol': {
        'module' : 'qrshare.HTTPServer',
        'class' : 'HTTPServer',
    },
    'protocol_params': {
        'ip': '127.0.0.1',
        'port': 7080
    },
    'view': {
        'module' : 'qrshare.QRView',
        'class' : 'QRView',
    },
    'view_params': {
    }
}

def get_user_config_json():
    """
    Retrieves the user's configuration as a JSON object.

    Returns:
        dict: A dictionary containing the user's configuration.

    Notes:
        The user's configuration is stored in a file on the local filesystem.
    """
    config_file_path = os.path.join(os.path.expanduser('~'), USER_CONFIG_JSON_NAME)
    try: 
        with open(config_file_path, 'r') as f:
            json_config = json.load(f)
            return json_config
    except Exception as e:
        print(f'Read user configuration failed with an error {e}, using default configuration')
        with open(config_file_path, 'w') as f:
            json.dump(default_json_file, f)
            return default_json_file

def validate_json(user_json):
    """
    Validates a user's JSON configuration.

    Args:
        user_json (dict): A dictionary containing the user's configuration.

    Raises:
        Exception: If the user's configuration is invalid.

    Notes:
        The user's configuration is considered valid if it has the following keys:
            - 'protocol'
            - 'view'
            - 'protocol_params'
            - 'view_params'
        The 'protocol' and 'view' keys should contain dictionaries with the following keys:
            - 'module'
            - 'class'
    """
    keys = ['protocol', 'view', 'protocol_params', 'view_params']
    
    for key in keys:
        if key not in user_json.keys():
            raise Exception(f'User json config has no field \'{key}\'')
    
    if 'module' not in user_json['protocol']:
        raise Exception('User json config has no field \'module\' in \'protocol\'')
    if 'class' not in user_json['protocol']:
        raise Exception('User json config has no field \'class\' in \'protocol\'')
    
    if 'module' not in user_json['view']:
        raise Exception('User json config has no field \'module\' in \'view\'')
    if 'class' not in user_json['view']:
        raise Exception('User json config has no field \'class\' in \'view\'')
    

def dynamic_import(module, class_name):
    """
    Dynamically imports a class from a module.

    Args:
        module (str): The name of the module to import.
        class_name (str): The name of the class to import.

    Returns:
        type: The imported class.

    Examples:
        >>> cls = dynamic_import('my_module', 'MyClass')
        >>> obj = cls()
    """
    mod = importlib.import_module(module)
    return getattr(mod, class_name)

def main():
    # TODO use argparse instead
    if len(sys.argv) <= 1:
        print('Please specify file to upload')
        return -1

    if len(sys.argv) != 2:
        print('Please provide one file only')
        return -1

    file_to_upload = sys.argv[-1]

    user_config = get_user_config_json()
    
    validate_json(user_config)
    
    client_class = dynamic_import(user_config['protocol']['module'], 
                                  user_config['protocol']['class'])
    client_params = user_config['protocol_params']
    try:
        client_class.validate_init_params(**client_params)
    except Exception as ex:
        raise Exception(f'params in user json config for protocol {client_class} are invalid, reason: {ex}')
        
    client = client_class(**client_params)
    
    view_class = dynamic_import(user_config['view']['module'], 
                                user_config['view']['class'])
    view_params = user_config['view_params']
    
    try:
        view_class.validate_init_params(**view_params)
    except Exception as ex:
        raise Exception(f'params in user json config for view {client_class} are invalid, reason: {ex}')
        
    view = view_class(**view_params)

    path = client.upload(file_to_upload)
    view.view(path)

if __name__ == '__main__':
    main()
