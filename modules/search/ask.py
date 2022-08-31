import asyncio
from pocx import AioPoc
from loguru import logger
from funcs.parser import extract_email


class Ask(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Ask, self).__init__()
        self.name = 'Ask'

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        # search_content = f'intext:%22%40{email}%22'
        # search_content = f'intext:%40{email}'
        search_content = f'%40{email}'
        emails = []
        page_num = 1
        per_page_num = 10
        limit_num = 50
        header = {
            'authority': 'www.ask.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Aoyou/OGd8YktaKlxxUCRbZDYuOwjUGDHTRP9_zPseVz9cQtPRb-W9amN9jfBl',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.ask.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.set_headers(headers=header)
        while True:
            url = f'https://www.ask.com/web?q={search_content}&page={page_num}'
            resp = await self.aio_get(url)
            if not resp:
                break
            if resp.status_code == 200:
                emails.extend(extract_email(email, resp.content.decode('utf-8')))
            else:
                logger.error(f'Ask module got an error, error code: {resp.status_code}. Stop page: {page_num}.')
                break
            page_num += 1
            # 搜索条数限制
            if page_num * per_page_num > limit_num:
                break
            await asyncio.sleep(1)
        if emails:
            emails = list(set(emails))
        logger.success(f'Ask module Found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    mw = Ask()
    mw.run('target.com')
