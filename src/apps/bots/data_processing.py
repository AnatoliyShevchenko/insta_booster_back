# FastApi
from fastapi import UploadFile

# Third-Party
import aiofiles

# Python
import os

# Local
from src.settings.const import VOLUME
from src.settings.base import logger
from .orm import BotsOrm
from .schemas import BotSchema


class DataProcessing:

    @staticmethod
    async def save_file_to_volume(file: UploadFile):
        file_path = os.path.join(VOLUME, file.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await out_file.write(chunk)
        return file_path

    @staticmethod
    async def get_chunks(file_path: str):
        orm = BotsOrm()
        lines = []
        try:
            async with aiofiles.open(file=file_path) as file:
                iteration = 0
                async for line in file:
                    if len(lines) >= 100:
                        await orm.create_bots_batch(bots_data=lines)
                        iteration += 1
                        logger.info(
                            msg=f"Iteration {iteration} success!"
                        )
                        lines.clear()
                    try:
                        username, password = line.split(" ")
                        schema = BotSchema(
                            username=username.strip(),
                            password=password.strip()
                        )
                        temp = schema.model_dump()
                        lines.append(temp)
                    except ValueError as ve:
                        logger.error(
                            f"Error processing line: {line.strip()} - {ve}"
                        )

                if lines:
                    await orm.create_bots_batch(bots_data=lines)
                    logger.info(msg="Last iteration success!")
            return "Success"
        except Exception as e:
            return str(e)
