# FastAPI
from fastapi import APIRouter, status, UploadFile, Response

# Local
from src.apps.abstract.schemas import ResponseSchema, ErrorSchema
from .schemas import BotSchema, BotsSchema
from .orm import BotsOrm
from .data_processing import DataProcessing


class BotsView(DataProcessing):
    """View for Bots."""

    def __init__(self) -> None:
        self.path = "/bots/"
        self.orm = BotsOrm()
        self.router = APIRouter(prefix="/api/v1", tags=["View/Create Bots"])
        self.router.add_api_route(
            path=self.path+"{page_number}/", endpoint=self.get_bots,
            description="""Эндпоинт для просмотра ботов, с пагинацией. 
            Нумерация начинается с нуля""",
            methods=["GET"], responses={
                200: {"model": BotsSchema},
                204: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path, endpoint=self.post, 
            description="""Эндпоинт для создания ботов, 
            принимает текстовый файл с логинами и паролями, 
            лучше всего в формате txt. 
            Файл должен выглядеть примерно так: \n
            Логин Пароль\n
            Логин Пароль
            """,
            methods=["POST"], responses={
                200: {"model": ResponseSchema},
                500: {"model": ErrorSchema},
            }
        )

    async def get_bots(self, page_number: int):
        bots = await self.orm.get_bots(offset=page_number)
        if not bots:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        data = []
        for bot in bots:
            temp = BotSchema(
                username=bot.username, password=bot.password
            )
            data.append(temp)
        return BotsSchema(page=page_number, bots=data)
        
    async def post(self, response: Response, file: UploadFile):
        file_path = await self.save_file_to_volume(file=file)
        result = await self.get_chunks(file_path=file_path)
        if result == "Success":
            return ResponseSchema(response=result)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorSchema(error=result)


bots = BotsView()
