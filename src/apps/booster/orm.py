# SQLAlchemy
from sqlalchemy import select, update, and_, insert

# Python
from typing import Literal

# Local
from src.settings.base import session, logger
from .models import Actions, ActionData


class ActionsOrm:
    """ORM for actions."""

    @staticmethod
    async def create_action(link: str, action: str, type_action: str):
        try:
            async with session() as conn:
                async with conn.begin():
                    stmt = insert(Actions).values(
                        link=link, action=action, type_action=type_action
                    ).returning(Actions)
                    result = await conn.execute(statement=stmt)
                    obj = result.scalars().first()
                    data = ActionData(
                        id=obj.id, link=obj.link, action=obj.action,
                        type_action=obj.type_action
                    )
                await conn.commit()
            return data
        except Exception as e:
            logger.error(msg="Cannot create action:", exc_info=e)
            return f"Cannot create action: {e}"

    @staticmethod
    async def activate_action(action_id: int):
        try:
            async with session() as conn:
                stmt = (update(Actions).where(
                    Actions.id == action_id
                ).values(in_progress=True))
                await conn.execute(statement=stmt)
                await conn.commit()
            return True
        except Exception as e:
            logger.error(
                msg=f"Cannot activate action_{action_id}:", exc_info=e
            )
            return False

    @staticmethod
    async def finish_action(action_id: int):
        try:
            async with session() as conn:
                stmt = (update(Actions).where(
                    Actions.id == action_id
                ).values(is_done=True))
                await conn.execute(statement=stmt)
                await conn.commit()
            return True
        except Exception as e:
            logger.error(
                msg=f"Cannot finish action_{action_id}:", exc_info=e
            )
            return False

    @staticmethod
    async def get_actions_by_state(
        state: Literal["done", "in_progress", "unactive"],
        type_action: Literal["Photo", "Reels"],
        limit: int = 100, offset: int = 0
    ):
        async with session() as conn:
            query = select(Actions)
            if state == "done":
                query = query.where(and_(
                    Actions.is_done == True,
                    Actions.type_action == type_action
                ))
            elif state == "in_progress":
                query = query.where(and_(
                    Actions.in_progress == True,
                    Actions.type_action == type_action
                ))
            elif state == "unactive":
                query = query.where(and_(
                    Actions.is_done == False,
                    Actions.in_progress == False,
                    Actions.type_action == type_action
                ))

            data = await conn.execute(query.limit(limit).offset(offset))
            result = data.scalars().all()
        if result:
            return result
        else:
            return None
    