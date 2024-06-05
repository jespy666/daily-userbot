from abc import ABC, abstractmethod

from typing import Dict, Any, Optional


class AsyncBase(ABC):

    @abstractmethod
    async def fetch_one(self, field: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def fetch_all(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update_one(self, field: str, new_value: Any) -> None:
        pass
