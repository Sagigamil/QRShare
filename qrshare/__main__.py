import os
import sys
import json
import importlib


USER_CONFIG_JSON_NAME = 'qrshare_config.json'

default_json_file = {
    "protocol": "qrshare.HTTPServer.HTTPServer",
    "protocol_params": {
        "ip": "127.0.0.1",
        "port": 7080
    },
    "view": "qrshare.QRView.QRView",
    "view_params": {
    }
}


def get_user_config_json():
    config_file_path = os.path.join(os.path.expanduser('~'), USER_CONFIG_JSON_NAME)
    try: 
        with open(config_file_path, 'r') as f:
            json_config = json.load(f)
            return json_config
    except Exception as e:
        print(f"Read user configuration failed with an error {e}, using default configuration")
        with open(config_file_path, 'w') as f:
            json.dump(default_json_file, f)
            return default_json_file


# Load python class by it's name dynamically
# Load python class by it's name dynamically
def dynamic_import(module):
    module_name, class_name = module.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


def main():
    # TODO use argparse instead
    if len(sys.argv) <= 1:
        print("Please specify file to upload")
        return -1

    if len(sys.argv) != 2:
        print("Please provide one file only")
        return -1

    file_to_upload = sys.argv[-1]

    user_config = get_user_config_json()
    import ipdb; ipdb.set_trace()
    client_class = dynamic_import(user_config['protocol'])
    client_params = user_config['protocol_params']
    client = client_class(**client_params)
    
    view_class = dynamic_import(user_config['view'])
    view_params = user_config['view_params']
    view = view_class(**view_params)

    path = client.upload(file_to_upload)
    view.view(path)


if __name__ == "__main__":
    main()
