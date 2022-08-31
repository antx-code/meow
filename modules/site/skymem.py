import asyncio
from pocx import AioPoc
from loguru import logger
import re
from funcs.parser import extract_email


class Skymem(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Skymem, self).__init__()
        self.name = 'SkyMem'

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        emails = []
        first_url = f'https://www.skymem.info/srch?q={email}&ss=srch'
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Aoyou/R0dwN2AqeFhWC2FdImhDMtYPbepzCaq2ExzA-PnBDq2QBC-jrWu35ZNZ'
        }
        self.set_headers(headers=header)
        resp = await self.aio_get(first_url)
        try:
            domain_id = re.findall('domain\/(.*)\?p=2', resp.text)[0]
            domain_url = f'https://www.skymem.info/domain/{domain_id}?p='
            all_domain_nums = re.findall(f"<title>q={email} - {email}=(.*) emails</title>", resp.text)[0]
            domain_resp = await self.aio_get(domain_url + '1')
            loop_num = re.findall(f"This is the preview, first (.*) emails", domain_resp.text)[0]
            # logger.success(f'all email nums:{all_domain_nums}, free num: {loop_num}')
            loop = int(loop_num)
            if loop % 5 == 0:
                loop = int(loop / 5)
            else:
                loop = int(loop / 5) + 1
            for i in range(1, loop + 1):
                r = await self.aio_get(domain_url + str(i))
                targets = extract_email(email, r.text)
                emails.extend(targets)
                await asyncio.sleep(1)
        except Exception as e:
            targets = extract_email(email, resp.content.decode('utf-8'))
            emails.extend(targets)
        emails = list(set(emails))
        logger.success(f'SkyMem module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    mw = Skymem()
    mw.run('target.com')
