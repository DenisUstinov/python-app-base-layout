import logging
import asyncio

import config
import app

settings = app.Settings.from_config(config.config)

app.setup_logger(settings)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting app...")

    service = None
    try:
        storage = app.Storage(settings.STORAGE_PATH)
        await storage.create_table()

        service = app.Service(settings, app.Client(), app.Handler(), storage)
        
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