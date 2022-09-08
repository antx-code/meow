import asyncio
import uvloop
from loguru import logger
import typer
import importlib
import os
import time
from funcs.fileio import save2file

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
uvloop.install()
app = typer.Typer(help='Antx Fast and Powerful Email Finder Tool')


def _load_files(modules):
    modules = modules if isinstance(modules, list) else [modules]
    files = []
    module_path = f'{os.path.dirname(__file__)}/modules'
    for module in modules:
        filelist = os.listdir(f'{module_path}/{module}')
        for file in filelist:
            if '__' in file or 'pwned' in file:
                continue
            files.append(file.split(".py")[0])
    return files


def _load_module():
    objects = []
    modules = ['site', 'search']
    for module in modules:
        files = _load_files(module)
        for file in files:
            mod = file.capitalize()
            try:
                logger.debug(f'Loading modules.{module}.{file} module')
                package = importlib.import_module(f"modules.{module}.{file}")
                objects.append(getattr(package, mod)())
            except ImportError:
                logger.warning(f'Loading modules.{module}.{file} module')
                package = importlib.import_module(f".{file}", package=f'modules.{module}')
                objects.append(getattr(package, mod)())
    return objects


@logger.catch(level='ERROR')
async def aio_dia(target: str, is_save: bool = False):
    logger.info(f'Welcome to Antx Email Finder Tool.')
    logger.debug(f'Starting find {target} ......')
    emails = []
    email_list = []
    objs = _load_module()
    start = time.time()
    for obj in objs:
        obj_emails = await obj.poc(target)
        if not obj_emails:
            continue
        emails.extend(obj_emails)
    emails = list(set(emails))
    for email in emails:
        if len(email.split('@')[0]) < 2:
            continue
        email_list.append(email)
    if is_save:
        save2file(f'{target}_email_success', email_list)
    end = time.time()
    logger.success(f'Found {len(email_list)} emails.')
    logger.success(f'Emails: {email_list}')
    logger.success(f'All Task has been finished, cost {end - start} seconds.')
    return email_list


@logger.catch(level='ERROR')
@app.command()
def dia(target: str):
    logger.info(f'Welcome to Antx Email Finder Tool.')
    logger.debug(f'Starting find {target} ......')
    emails = []
    email_list = []
    objs = _load_module()
    start = time.time()
    for obj in objs:
        obj_emails = obj.dia(target)
        if not obj_emails:
            continue
        emails.extend(obj_emails)
    emails = list(set(emails))
    for email in emails:
        if len(email.split('@')[0]) < 2:
            continue
        email_list.append(email)
    save2file('email_success', email_list)
    end = time.time()
    logger.success(f'Found {len(email_list)} emails.')
    logger.success(f'Emails: {email_list}')
    logger.success(f'All Task has been finished, cost {end - start} seconds.')
    return email_list


if __name__ == '__main__':
    app()
