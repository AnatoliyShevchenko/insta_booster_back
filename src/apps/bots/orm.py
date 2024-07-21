# SQLAlchemy
from sqlalchemy import select

# Local
from src.settings.base import session, logger
from .models import Bots


class BotsOrm:
    """ORM for bots."""

    @staticmethod
    async def create_bot(username: str, password: str) -> bool:
        try:
            async with session() as conn:
                async with conn.begin():
                    obj = Bots(
                        username=username, password=password
                    )
                    conn.add(instance=obj)
                    await conn.commit()
            return True
        except Exception as e:
            logger.error(msg="Cannot create bot:", exc_info=e)
            return False
    
    @staticmethod
    async def get_bots(
        limit: int = 100, offset: int = 0
    ):
        async with session() as conn:
            users = await conn.execute(
                select(Bots).limit(limit).offset(offset)
            )
            result = users.scalars().all()
        return result
    
    @staticmethod
    async def get_all_bots():
        async with session() as conn:
            users = await conn.execute(select(Bots))
            result = users.scalars().all()
        return result
    
    @staticmethod
    async def create_bots_batch(
        bots_data: list[dict[str, str]]
    ) -> bool:
        try:
            async with session() as conn:
                async with conn.begin():
                    bots = [Bots(**data) for data in bots_data]
                    conn.add_all(bots)
                    await conn.commit()
            return True
        except Exception as e:
            logger.error(msg="Cannot create bots batch:", exc_info=e)
            return False
