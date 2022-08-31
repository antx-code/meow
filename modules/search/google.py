import asyncio
from pocx import AioPoc
from loguru import logger
from funcs.parser import extract_google


class Google(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Google, self).__init__()
        self.name = 'Google'

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        # search_content = f'intext:%22%40{email}%22'
        search_content = f'intext:%40{email}'
        # search_content = f'%40{email}'
        page_num = 1
        per_page_num = 10
        limit_num = 100
        emails = []
        header = {
            'authority': 'www.google.com.hk',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'dnt': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'x-client-data': 'CIa2yQEIpLbJAQipncoBCOCNywEIlaHLAQiljswBCMbGzAEYq6nKAQ==',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-full-version': '"99.0.4844.74"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-ua-platform-version': '"5.15.32"',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version-list': '" Not A;Brand";v="99.0.0.0", "Chromium";v="99.0.4844.74", "Google Chrome";v="99.0.4844.74"',
            'referer': 'https://www.google.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.set_headers(headers=header)
        while True:
            offset = (page_num - 1) * per_page_num
            url = f"https://www.google.com.hk/search?q={search_content}&start={offset}&num={per_page_num}&filter=0&btnG=Search&gbv=1&hl=en&dpr=1"
            resp = await self.aio_get(url)
            if not resp:
                break
            if resp.status_code == 200:
                emails.extend(extract_google(email, resp.content.decode('utf-8')))
            else:
                logger.error(f'Google module got an error, error code: {resp.status_code}. Stop page: {page_num}.')
                break
            page_num += 1
            # 搜索条数限制
            if page_num * per_page_num > limit_num:
                break
            await asyncio.sleep(1)
        if emails:
            emails = list(set(emails))
        logger.success(f'Google module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    mw = Google()
    mw.run('target.com')
