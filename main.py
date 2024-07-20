# Third-Party
import uvicorn

# Local
from src.apps.bots.views import bots
from src.settings.base import app


app.include_router(router=bots.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
