import yaml


def load_yaml(file: str) -> yaml:
    with open(file, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)  # Always safe_load or code can be injected from yaml ?
