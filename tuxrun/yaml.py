import yaml


try:
    from yaml import CFullLoader as FullLoader  # type: ignore
except ImportError:
    from yaml import FullLoader

    print("Warning: using python yaml loader")


def yaml_load(data):
    return yaml.load(data, Loader=FullLoader)
