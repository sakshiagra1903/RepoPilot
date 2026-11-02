import httpx
from .config import settings
BASE='https://api.github.com'
class GitHubError(Exception): pass
class GitHub:
    def __init__(self,token_value=None):
        self.headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
        token_value=token_value or settings.github_token
        if token_value: self.headers['Authorization']=f'Bearer {token_value}'
    async def get(self,path,params=None):
        async with httpx.AsyncClient(timeout=25,headers=self.headers,follow_redirects=True) as client:
            response=await client.get(BASE+path,params=params)
            if response.status_code==404: raise GitHubError('Repository or resource not found, or access was not granted.')
            if response.status_code==403: raise GitHubError('GitHub rate limit or permission denied. Configure a token with read access.')
            if response.status_code>=400: raise GitHubError(f'GitHub API returned HTTP {response.status_code}.')
            return response.json()
    async def pages(self,path,params=None,limit=100):
        out=[]
        for page in range(1,4):
            data=await self.get(path,{**(params or {}),'per_page':min(limit,100),'page':page})
            if not isinstance(data,list): return data
            out.extend(data)
            if len(data)<min(limit,100): break
        return out[:limit]
