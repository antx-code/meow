import asyncio
from pyhunter import PyHunter
from loguru import logger
from conf import CONF


class Hunter():
    @logger.catch(level='ERROR')
    def __init__(self):
        self.apikey = CONF['Hunter']
        self.hunter = PyHunter(self.apikey)

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        email = target.split('@')[1] if '@' in target else target
        emails = []
        try:
            results = self.hunter.domain_search(email)
            for result in results['emails']:
                emails.append(result['value'])
        except Exception as e:
            if '401 Client Error: Unauthorized' in str(e):
                logger.error(f'Invalid Hunter API key.')
            if '429 Client Error: Too Many Requests' in str(e):
                logger.error(f'Free search count for hunter was used up.')
        logger.success(f'Hunter module found {len(emails)} emails.')
        return emails

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    email = 'target.com'
    mw = Hunter()
    asyncio.run(mw.poc(email))
