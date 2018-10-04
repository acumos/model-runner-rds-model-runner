import configparser
import logging
import os


class ConfigUtilException(Exception):
    pass


def get_properties_path():
    if 'PROPERTIES_PATH' in os.environ:
        properties_path = 'properties'  # we assume relative
    properties_path = os.environ.get('PROPERTIES_PATH', 'properties')
    if not os.path.exists(properties_path):
        raise ConfigUtilException(f'{properties_path} does not exist. Please set PROPERTIES_PATH environmental value')
    return properties_path


_parser = None  # cache parser to avoid constant file IO


def get_parser():
    global _parser
    if _parser is None:
        parser = configparser.ConfigParser()
        # TODO (pk9069): allow settings.cfg to be specified
        config_path = os.path.join(get_properties_path(), 'settings.cfg')
        logging.info("config_path: %s", config_path)
        parser.read(config_path)
        _parser = parser
    return _parser


def get_config_value(env_name, config=None, config_name=None, section=None):
    if env_name in os.environ:
        return os.environ[env_name]

    if config is None:
        config = get_parser()
    if section is not None:
        if section not in config:
            raise ConfigUtilException(f"Section {section} does not exist")
        config = config[section]
    if config_name is None:
        config_name = env_name
    if config_name in config:
        return config[config_name]
    raise ConfigUtilException(f"Configurable {env_name} not in environment nor configuration")


def verify_ssl():
    return os.environ.get('VERIFY_SSL', 'true').lower() != 'false'


def get_model_cache_dir():
    return get_config_value('model_cache_dir', section='MODEL_CACHE')
