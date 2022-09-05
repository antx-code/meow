import asyncio
from pocx import AioPoc
from loguru import logger
import json
from funcs.parser import extract_email
from conf import CONF


class Giteees(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(Giteees, self).__init__()
        self.name = 'Gitee Email Search'
        self.gitee_token = CONF['Gitee']

    @logger.catch(level='ERROR')
    async def ping(self):
        resp = await self.aio_get(f'https://gitee.com/api/v5/search/repositories?access_token={self.gitee_token}&q=%40baidu.com')
        if resp.status_code == 200:
            return True
        else:
            if resp.status_code == 401:
                logger.error('Gitee Token is invalid, please check your gitee Token.')
            return False

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        search_content = f'%40{email}'
        scopes = ['repositories', 'issues', 'users']
        emails = []
        page_num = 1
        per_page_num = 50
        limit_num = 500
        if not await self.ping():
            logger.success(f'Gitee module found {len(emails)} emails.')
            return []
        for scope in scopes:
            while True:
                base_url = f'https://gitee.com/api/v5/search/{scope}?access_token={self.gitee_token}&q={search_content}&page={page_num}&per_page={per_page_num}&order=desc'
                resp = await self.aio_get(base_url)
                if not resp:
                    break
                items = json.loads(resp.text)
                if not items:
                    break
                for item in items:
                    emails.extend(extract_email(email, str(item)))
                page_num += 1
                # 搜索条数限制
                if page_num * per_page_num > limit_num:
                    break
                await asyncio.sleep(0.5)
        if emails:
            emails = list(set(emails))
        logger.success(f'Gitee module found {len(emails)} email.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    mw = Giteees()
    mw.run('target.com')
