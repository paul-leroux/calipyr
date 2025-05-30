

import configparser
from pathlib import Path

def load_config(config_file="config/settings.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

# Optional convenience: get paths as Path objects
def get_paths(config):
    base = Path(__file__).resolve().parent.parent
    data_dir = base / config["paths"]["data_dir"]
    output_dir = base / config["paths"]["output_dir"]
    figures_dir = base / config["paths"]["figures_dir"]
    return data_dir, output_dir, figures_dir
