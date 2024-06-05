from typing import Dict, Any, Optional

from motor.motor_asyncio import AsyncIOMotorClient

from ..base import AsyncBase
from config import DBConfig


class AsyncMongoManager(AsyncBase):

    def __init__(self, db_config: DBConfig, db_collection: str) -> None:
        super().__init__()
        self.client = AsyncIOMotorClient(db_config.get_db_url())
        self.db_name = self.client[db_config.db_name]
        self.db_collection = self.db_name[db_collection]

    async def fetch_one(self, field: str) -> Optional[Any]:
        document: Dict[str, Any] = await self.db_collection.find_one()
        return document.get(field)

    async def fetch_all(self) -> Dict[str, Any]:
        document: Dict[str, Any] = await self.db_collection.find_one()
        return document

    async def update_one(self, field: str, new_value: Any) -> None:
        await self.db_collection.update_one(
            {},
            {'$set': {field: new_value}}
        )
