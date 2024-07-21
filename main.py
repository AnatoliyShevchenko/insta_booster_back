# Third-Party
import uvicorn
import asyncio

# Python
import threading

# Local
from src.apps.bots.views import bots
from src.apps.booster.views import create, view
from src.settings.base import app, scheduler, AIOREDIS, logger


def start_scheduler():
    # Создаем новый цикл событий в этом потоке
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler.start()
    # Запускаем цикл событий для шедулера
    loop.run_forever()


async def main():
    app.include_router(router=bots.router)
    app.include_router(router=create.router)
    app.include_router(router=view.router)
    scheduler_thread = threading.Thread(
        target=start_scheduler, daemon=True
    )
    scheduler_thread.start()
    config = uvicorn.Config(
        app="main:app", host="0.0.0.0", port=8050
    )
    server = uvicorn.Server(config=config)
    logger.info(msg="SERVER STARTED")
    await server.serve()

async def shutdown():
    await AIOREDIS.aclose()
    logger.info(msg="SHUTDOWN SERVER")

    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.run(shutdown())
