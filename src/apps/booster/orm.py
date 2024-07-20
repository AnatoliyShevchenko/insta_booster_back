# SQLAlchemy
from sqlalchemy import select, update
from sqlalchemy import Sequence

# Local
from src.settings.base import session, logger
from .models import Actions


class ActionsOrm:
    """ORM for actions."""

    @staticmethod
    async def create_action(link: str, action: str):
        pass

    @staticmethod
    async def get_first_active_action():
        pass

    @staticmethod
    async def finish_action(action_id: int):
        pass
