import asyncio
from pocx import AioPoc
from loguru import logger
from funcs.parser import extract_email


class Baidu(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Baidu, self).__init__()
        self.name = 'Baidu'

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        # search_content = f'intext:%22%40{email}%22'
        # search_content = f'intext:%40{email}'
        search_content = f'%40{email}'
        emails = []
        page_num = 0
        per_page_num = 10
        limit_num = 500
        header = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': f'https://www.baidu.com/s?wd={search_content}%2&pn=0&oq={search_content}%20-baijiahao&ie=utf-8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.set_headers(headers=header)
        while True:
            url = f"https://www.baidu.com/s?wd={search_content}&rn={per_page_num}&pn={page_num * per_page_num}&ie=utf-8"
            resp = await self.aio_get(url)
            if not resp:
                break
            if resp.status_code == 200:
                emails.extend(extract_email(email, resp.content.decode('utf-8')))
            else:
                logger.error(f'Baidu module got an error, error code: {resp.status_code}. Stop page: {page_num}.')
                break
            page_num += 1
            # 搜索条数限制
            if page_num * per_page_num > limit_num:
                break
            await asyncio.sleep(1)
        if emails:
            emails = list(set(emails))
        logger.success(f'Baidu module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    mw = Baidu()
    mw.run('target.com')
