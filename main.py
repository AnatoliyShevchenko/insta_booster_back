# Third-Party
import uvicorn

# Local
from src.apps.bots.views import bots
from src.apps.booster.views import actions
from src.settings.base import app


app.include_router(router=bots.router)
app.include_router(router=actions.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
