from loguru import logger
import os


@logger.catch(level='ERROR')
def save2file(filename, content, filetype: str = 'csv'):
    contents = [content] if isinstance(content, str) else content
    output_path = f'{os.path.dirname(__file__)}/output'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(f'{output_path}/{filename}.{filetype}', 'a+', encoding='utf-8') as f:
        for content in contents:
            f.write(f'{content}\n')
        f.close()
