import asyncio
from pocx import AioPoc
from loguru import logger
from gitlab import Gitlab, const
from funcs.parser import extract_email
from conf import CONF


class GitlabES(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(GitlabES, self).__init__()
        self.name = 'Gitlab Email Search'
        self.gitlab_token = CONF['Gitlab']

    @logger.catch(level='ERROR')
    def ping(self):
        gl = Gitlab(private_token=self.gitlab_token)
        try:
            gl.auth()
            return True
        except Exception as e:
            if '401' in str(e):
                logger.error(f'Gitlab token is invalid.')
            return False

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        search_content = f'@{email}'
        results = []
        per_page_num = 10
        limit_num = 100
        gl = Gitlab(private_token=self.gitlab_token)
        if not self.ping():
            return 0, []
        for scope in const.SearchScope:
            logger.debug(f'scope: {scope}')
            page_num = 1
            for item in gl.search(scope, search_content, iterator=True):
                # 搜索条数限制
                if page_num * per_page_num > limit_num:
                    break
                if scope == 'commits':
                    results.extend([item['author_email'], item['committer_email']])
                    page_num += 1
                    continue
                results.extend(extract_email(email, str(item)))
                page_num += 1
                await asyncio.sleep(0.5)
        if 'none@none' in results:
            results.remove('none@none')
        results = list(set(results))
        total_count = len(results)
        logger.success(f'Gitlab module found {total_count} emails.')
        return total_count, results

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    # https://docs.gitlab.com/ee/api/search.html
    # https://python-gitlab.readthedocs.io/en/stable/gl_objects/search.html
    mw = GitlabES()
    mw.run('target.com')
