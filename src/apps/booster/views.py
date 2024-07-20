# FastAPI
from fastapi import APIRouter, status, Response

# Local
from src.apps.abstract.schemas import ResponseSchema, ErrorSchema
from .schemas import ActionSchema
from .orm import ActionsOrm


class ActionsView:
    """View for Actions."""

    def __init__(self) -> None:
        self.path = "/actions"
        self.orm = ActionsOrm()
        self.router = APIRouter(prefix="/api/v1", tags=["Create Actions"])
        self.router.add_api_route(
            path=self.path+"/photo/", endpoint=self.photo_action, 
            description="""Эндпоинт для "создания заявки" на буст фото. 
            принимает аргументы: \n
            - link - ссылка на фото,\n
            - action - действие, одно из [Likes, Comments].""",
            methods=["POST"], responses={
                200: {"model": ResponseSchema},
                500: {"model": ErrorSchema},
            }
        )

    async def photo_action(self, schema: ActionSchema):
        pass


actions = ActionsView()
