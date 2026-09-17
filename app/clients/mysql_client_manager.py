from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from app.conf.app_config import app_config, DBConfig
import asyncio
from sqlalchemy import text
class MysqlClientManager:
    def __init__(self, db_config: DBConfig):
        self.engine: AsyncEngine = None
        self.db_config = db_config
    def _get_url(self):
        return f"mysql+asyncmy://{self.db_config.user}:{self.db_config.password}@{self.db_config.host}:{self.db_config.port}/{self.db_config.database}?charset=utf8mb4"
    def init(self):
        self.engine = create_async_engine(self._get_url())
    async def close(self):
        # 释放数据库连接
        await self.engine.dispose()

dw_mysql_client_manager = MysqlClientManager(app_config.db_dw)
meta_mysql_client_manager = MysqlClientManager(app_config.db_meta)

if __name__ == "__main__":
    dw_mysql_client_manager.init()
    engine = dw_mysql_client_manager.engine
    async def test():
        async with AsyncSession(engine) as session:
            result = await session.execute(text("select * from dim_customer limit 10"))
            rows = result.fetchall()
            for row in rows:
                print(row)
    asyncio.run(test())