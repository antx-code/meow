import asyncio
from loguru import logger
from pocx import AioPoc
from funcs.parser import extract_email


class Emailformat(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Emailformat, self).__init__()
        self.name = 'EmailFormat'

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        emails = []
        url = f'https://www.email-format.com/d/{email}/'
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Aoyou/R0dwN2AqeFhWC2FdImhDMtYPbepzCaq2ExzA-PnBDq2QBC-jrWu35ZNZ'
        }
        self.set_headers(headers=header)
        resp = await self.aio_get(url, headers=header)
        if not resp:
            return emails
        if resp.status_code == 200:
            emails = extract_email(email, resp.content.decode('utf-8'))
            emails = list(set(emails))
        else:
            logger.error(f'EmailFormat module got an error, error code: {resp.status_code}.')
        logger.success(f'EmailFormat module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    mw = Emailformat()
    mw.run('target.com')
