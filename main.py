import logging
import asyncio

import config
import app

settings = app.Settings.build(config.CONFIG)

app.setup_logger(settings)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting app...")

    service = None
    try:
        client = app.Client()

        handler = app.Handler(client, settings.HANDLER)
        
        storage = app.Storage(settings.STORAGE)
        await storage.initialize()

        service = app.Service(client, app.Parser(), handler, storage)
        
        async with asyncio.TaskGroup() as tg:
            tg.create_task(service.run())
    except* Exception as e:
        logger.critical(f"Service crashed: {e}", exc_info=True)
    finally:
        if service is not None:
            try:
                await service.shutdown()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}", exc_info=True)
            logger.info("App complete!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)