# FastAPI
from fastapi import APIRouter, status, UploadFile, Response

# Local
from src.apps.abstract.schemas import ResponseSchema, ErrorSchema
from .orm import BotsOrm
from .data_processing import DataProcessing


class BotsView(DataProcessing):
    """View for Bots."""

    def __init__(self) -> None:
        self.path = "/bots/"
        self.orm = BotsOrm()
        self.router = APIRouter(prefix="/api/v1", tags=["Create Bots"])
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

    async def post(self, response: Response, file: UploadFile):
        file_path = await self.save_file_to_volume(file=file)
        result = await self.get_chunks(file_path=file_path)
        if result == "Success":
            return ResponseSchema(response=result)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorSchema(error=result)


bots = BotsView()
