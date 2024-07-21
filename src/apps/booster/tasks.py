# Python
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# Local
from src.settings.base import scheduler, logger
from .reels import ActionsWithReels
from .photo import ActionsWithPhoto
from .orm import ActionsOrm
from src.apps.bots.orm import BotsOrm
from src.apps.bots.models import Bots
from .models import ActionData


class BoosterTasks:

    def __init__(self) -> None:
        self.orm = ActionsOrm()
        self.help_orm = BotsOrm()

    @staticmethod
    def bot_goes(action: ActionData, bot: Bots):
        try:
            if action.type_action == "Photo":
                obj = ActionsWithPhoto(
                    username=bot.username, password=bot.password
                )
            elif action.type_action == "Reels":
                obj = ActionsWithReels(
                    username=bot.username, password=bot.password
                )
            driver = obj.login_instagram()
            obj.get_action(
                driver=driver, link=action.link, 
                action=action.action
            )
        except:
            pass

    async def start_attack(self, action: ActionData):
        bots = await self.help_orm.get_all_bots()
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(self.bot_goes, action, bot)
                for bot in bots
            ]
            for future in futures:
                try:
                    future.result()
                    await self.orm.finish_action(action_id=action.id)
                except Exception as e:
                    logger.error(f"Thread encountered an error: {e}")
            
    async def start_booster_action(self, action: ActionData):
        start = datetime.now() + timedelta(seconds=10)
        activate = await self.orm.activate_action(action_id=action.id)
        if activate:
            scheduler.add_job(
                func=self.start_attack, trigger="date", args=(action,),
                id=f"{action.id}_{action.action}", run_date=start,
                name=f"{action.id}_{action.action}",
                misfire_grace_time=None, replace_existing=True,
                jobstore="redis"
            )
