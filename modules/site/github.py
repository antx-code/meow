import asyncio
from pocx import AioPoc
from loguru import logger
import base64
from conf import CONF
from funcs.parser import extract_email


class Github(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Github, self).__init__()
        self.name = 'Github'
        self.github_token = CONF['Github']

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        # search_content = f'intext:%22%40{email}%22'
        # search_content = f'intext:%40{email}'
        search_content = f'%40{email}'
        emails = []
        page_num = 1
        per_page_num = 100
        limit_num = 1000
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Aoyou/R0dwN2AqeFhWC2FdImhDMtYPbepzCaq2ExzA-PnBDq2QBC-jrWu35ZNZ',
            'Accept': 'application/vnd.github.v3.text-match+json',
            'Authorization': f"token {self.github_token}"
        }
        self.set_headers(headers=header)
        while True:
            url = f'https://api.github.com/search/code?q={search_content}&page={page_num}&per_page={per_page_num}&sort=indexed&order=desc'
            resp = await self.aio_get(url)
            if not resp:
                break
            if resp.status_code == 200:
                items = resp.json()['items']
                if not items:
                    break
                content_urls = [item['url'] for item in items]
                for content_url in content_urls:
                    rep = await self.aio_get(content_url.split('?')[0])
                    try:
                        content = rep.json()['content']
                        content = base64.b64decode(content).decode()
                        emails.extend(extract_email(email, content))
                    except Exception as e:
                        logger.error(f'Github module got an error, error code: {resp.status_code}. Stop page: {page_num}.')
                        break
            elif resp.status_code == 401:
                logger.error('Invalid github access token for credentials.')
                break
            else:
                logger.error(f'Github module got an error, error code: {resp.status_code}. Stop page: {page_num}.')
                break
            page_num += 1
            # 搜索条数限制
            if page_num * per_page_num > limit_num:
                break
            await asyncio.sleep(1)
        if emails:
            emails = list(set(emails))
        logger.success(f'Github module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    # https://docs.github.com/en/rest/search#search-code
    mw = Github()
    mw.run('target.com')
