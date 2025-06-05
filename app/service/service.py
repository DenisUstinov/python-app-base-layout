import logging

from .app_data import AppData

logger = logging.getLogger(__name__)

class Service:
    def __init__(self, client, parser, storage):
        self.ad = AppData(client, parser, storage)

    async def run(self):
        pass

    async def shutdown(self):
        logger.info("Shutting down Html...")
        await self.storage.close()
        await self.client.close()
        logger.info("Html shut down complete.")