import asyncio
from pocx import AioPoc
from loguru import logger
from funcs.parser import extract_email


class Pgp(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Pgp, self).__init__()
        self.name = 'Pgp'

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        emails = []
        url = f'https://pgp.mit.edu/pks/lookup?search={email}&op=index'
        header = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        self.set_headers(headers=header)
        resp = await self.aio_get(url)
        if not resp:
            return emails
        if resp.status_code == 200:
            emails = extract_email(email, resp.content.decode('utf-8'))
            emails = list(set(emails))
        elif resp.status_code == 404:
            pass
        else:
            logger.error(f'Pgp module got an error, error code: {resp.status_code}.')
        logger.success(f'Pgp module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    mw = Pgp()
    mw.run('target.com')
