import asyncio

from elasticsearch import AsyncElasticsearch

from app.conf.app_config import ESConfig, app_config


class ESClientManager:
    def __init__(self, config: ESConfig):
        self.client: AsyncElasticsearch | None = None
        self.config: ESConfig = config
    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"
    def init(self):
        self.client = AsyncElasticsearch(hosts=[self._get_url()])
    async def close(self):
        await self.client.close()
es_client_manager = ESClientManager(app_config.es)

if __name__ == '__main__':
    es_client_manager.init()
    client =es_client_manager.client
    # 这个函数是协程函数 todo
    async def test():
        # await client.indices.create(
        #     index='books',
        # )
        # await 只能出现在异步上下文中 todo
        await client.index(
            index='books',
            document={
                'name': 'Snow Crash',
                'author': 'Neal stephenson',
                'release_date': '1992-06-01',
                'page_count': 470,

            }
        )
        resp = await client.search(
            index='books',
        )
        print(resp)
        await es_client_manager.client.close()
    asyncio.run(test())