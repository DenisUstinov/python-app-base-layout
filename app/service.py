import asyncio
import logging

logger = logging.getLogger(__name__)

class Service:
    def __init__(self, settings, client, handler, storage):
        self.settings = settings
        self.client = client
        self.storage = storage
        self.handler = handler

    async def _fetch_data(self, params: dict) -> dict:
        await asyncio.sleep(3)
        logger.info(f"Geted!")

    async def _save_data(self, processed_data: dict) -> None:
        await asyncio.sleep(3)
        logger.info(f"Saved!")

    async def _process(self, task_id: int) -> None:
        logger.info(f"Task {task_id} started")
        async with asyncio.TaskGroup() as tg:
            for i in range(3):
                tg.create_task(self._fetch_data({}))
        async with asyncio.TaskGroup() as tg:
            for i in range(3):
                tg.create_task(self._save_data({}))
        await asyncio.sleep(10)
        logger.info(f"Task {task_id} completed")

    async def run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            for i in range(10):
                tg.create_task(self._process(i))
    
    async def shutdown(self) -> None:
        logger.info("Shutting down service...")

        await self.storage.close()
        logger.info("Storage connection closed.")

        await self.client.close()
        logger.info("Client shut down.")

        logger.info("Service shut down complete.")