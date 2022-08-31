import asyncio
from loguru import logger
import json
from pocx import AioPoc


class Haveibeenpwned(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Haveibeenpwned, self).__init__()
        self.name = 'HaveIBeenPwned'

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        results = []
        try:
            username = email.split('@')[0]
            domain = email.split('@')[1]
            if not username:
                raise Exception
        except Exception as e:
            logger.error('Please use correct email address.')
            return
        url = f"https://api.haveibeenpwned.com/unifiedsearch/{username}%40{domain}"
        header = {
            'authority': 'api.haveibeenpwned.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Aoyou/QD1LdWQ3bGlYTyZZd0lGT28pP97rmibjq0G0y7RNi-yqHPQYXPKtcOS3',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.set_headers(header)
        resp = await self.aio_get(url)
        if resp.status_code == 200:
            results = json.loads(resp.text)['Breaches']
            logger.success(f'HaveIBeenPwned found {len(results)} records.')
            # logger.success(json.dumps(results, indent=2))
        elif resp.status_code == 404:
            logger.success(f'Your email is security!')
        else:
            logger.error(f'HaveIBeenPwned module got an error, error code: {resp.status_code}.')
        return results

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    email = 'target.com'
    mw = Haveibeenpwned()
    mw.run(email)
