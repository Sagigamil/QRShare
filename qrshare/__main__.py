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

def find_pythonw_executable_path():
    """Returns the file path of the 'pythonw.exe' executable.
    
    The function searches for the 'pythonw.exe' executable in the same 
    folder as the current Python executable, and returns the full file path.
    """
    pythonw_exe = 'pythonw.exe'
    folder = os.path.dirname(sys.executable)
    return os.path.join(folder, pythonw_exe)
    
def install_registry():
    """Modifies the Windows registry to allow for sharing files using QRShare from 
      the right-click menu in Windows Explorer.
    
    This function is only supported on Windows operating systems. 
    If it is run on a non-Windows system, it will print a message and exit the program with a status code of -1.
    
    The function writes the necessary registry entries to a file called 'qrshare.reg', 
    runs the file to update the registry, and then removes the file.
    """    
    if os.name != 'nt':
        print('This option is supported only on windows.')
        exit(-1)
    
    print("Update registry to allow you to share folders from windwos right click menu using QRShare")

    reg_file_path = 'qrshare.reg' 
    reg_file_content = f"""Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\Share with QRShare]
@="Share With QRShare"

[HKEY_CLASSES_ROOT\*\shell\Share with QRShare\command]
@="\\"{find_pythonw_executable_path()}\\" -m qrshare \\"%1\\""
"""

    with open(reg_file_path, 'w') as f:
        f.write(reg_file_content)
    
    os.system(reg_file_path)
    os.remove(reg_file_path)        

def print_usage():
    print('Usage: uploader.py [--easy-launch-install] file')
    print('Options:')
    print('  --easy-launch-install  Install easy launch registry keys')
    print('  -h, --help             Show this help message')

def main():
    """Main entry point for the QRShare program.
    
    This function performs the following tasks:
    - If the '--easy-launch-install' flag is present in the command-line arguments, 
      it calls the 'install_registry' function to modify the Windows registry.
    - If no file is provided as a command-line argument, 
      it prints an error message and exits with a status code of -1.
    - If more than one file is provided as a command-line argument, 
      it prints an error message and exits with a status code of -1.
    - If a single file is provided as a command-line argument, 
      it retrieves the user configuration from a JSON file, 
      imports the specified client and view classes, 
      and initializes them with the provided parameters. 
      It then uses the client to upload the file and the view to display the URL for the uploaded file.
    
    If any errors occur during the execution of this function, 
    it prints an error message and exits with a status code of -1.
    """
    try: 
        if '-h' in sys.argv or '--help' in sys.argv:
            print_usage()
            return 0
        
        if '--easy-launch-install' in sys.argv:
            install_registry() 
            return 0
        
        if len(sys.argv) <= 1:
            print_usage()
            return -1

        if len(sys.argv) != 2:
            print_usage()
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
    
    except Exception as ex:
        print(f"QRShare failed, reason: {ex}")
        exit(-1)
        

if __name__ == '__main__':
    main()
