import asyncio
from pocx import AioPoc
from loguru import logger
import base64
import time
from conf import CONF
from funcs.parser import extract_email
from github import Github


class Githubes(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Githubes, self).__init__()
        self.name = 'Github Email Search'
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
                    except ConnectionError:
                        logger.error(f'Github module got an connection error, error code: {resp.status_code}. Stop page: {page_num}. Continue...')
                        continue
                    except Exception as e:
                        logger.error(f'Github module got an error, error code: {resp.status_code}. Stop page: {page_num}. Break...')
                        break
            elif resp.status_code == 401:
                logger.error('Invalid github access token for credentials.')
                break
            elif resp.status_code == 403:
                logger.error('You have exceeded a secondary rate limit. Please wait a few minutes before you try again.')
                break
            else:
                logger.error(f'Github module got an error, error code: {resp.status_code}. Stop page: {page_num}.')
                break
            page_num += 1
            # ??????????????????
            if page_num * per_page_num > limit_num:
                break
            await asyncio.sleep(1)
        if emails:
            emails = list(set(emails))
        logger.success(f'Github module found {len(emails)} emails.')
        return emails

    def poc_pygithub(self, target: str):
        per_page_num = 100
        gh = Github(self.github_token, per_page=per_page_num)
        email = target.split('@')[1] if '@' in target else target
        search_content = f'@{email}'
        emails = []
        try:
            results = gh.search_code(search_content, sort='indexed', order='desc')
            total_count = 1000 if int(results.totalCount) > 1000 else int(results.totalCount)
            if total_count <= per_page_num:
                for result in results:
                    emails.extend(extract_email(email, result.decoded_content.decode('utf-8')))
                    time.sleep(1)
            else:
                count = total_count % per_page_num
                pages = (total_count // per_page_num) if count == 0 else (total_count // per_page_num) + 1
                for page in range(1, pages + 1):
                    for content in results.get_page(page):
                        emails.extend(extract_email(email, content.decoded_content.decode()))
                        time.sleep(1)
        except Exception as e:
            logger.error(f'PyGithub module got an error, exiting.')
        if emails:
            emails = list(set(emails))
        logger.success(f'PyGithub module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    # https://docs.github.com/en/rest/search#search-code
    # https://pygithub.readthedocs.io/en/latest/github.html?highlight=search_code#github.MainClass.Github.search_code
    mw = Githubes()
    mw.run('target.com')
    # mw.poc_pygithub('target.com')
