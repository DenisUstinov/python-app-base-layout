import asyncio
import logging

logger = logging.getLogger(__name__)

class AppData:
    def __init__(self, client, parser, storage):
        self.client = client
        self.parser = parser
        self.storage = storage

    async def _process(self, source):
        try:
            while True:
                response = await self.client.request("get", source["url"])
                if not response:
                    raise ValueError("No data retrieved from the URL.")
                
                extracted_data = self.parser.extract(response, source["selectors"])
                if not extracted_data:
                    raise ValueError("No data extracted.")

                for data in extracted_data:
                    transformed_response = await self.handler.transform(data)
                    if not transformed_response:
                        raise ValueError(f"Failed to transform data for data: {data}")
                    
                    saved = await self.storage.save_data(source["model"], transformed_response)
                    if not saved:
                        raise RuntimeError("Failed to save data to storage.")
                
                await asyncio.sleep(source["timeout"])
        except asyncio.CancelledError:
            logger.info(f"Html for {source['url']} cancelled.")
        except Exception as e:
            logger.error(f"Error in Html for {source['url']}: {e}")
