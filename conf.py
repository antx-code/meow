from loguru import logger
import yaml
import os

@logger.catch(level='ERROR')
def get_config():
    base_path = os.path.dirname(__file__)
    with open(f'{base_path}/config.yaml', 'r+', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

CONF = get_config()
