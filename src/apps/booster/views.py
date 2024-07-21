# FastAPI
from fastapi import APIRouter, status, Response

# Third-Party
import asyncio

# Local
from src.apps.abstract.schemas import ResponseSchema, ErrorSchema
from .schemas import (
    CreatePhotoActionSchema, RequestActionsSchema, 
    ResponseActionsSchema, ActionsSchema,
)
from .orm import ActionsOrm
from .tasks import BoosterTasks


class CreateActionsView:
    """View for Actions."""

    def __init__(self) -> None:
        self.path = "/actions/create/"
        self.orm = ActionsOrm()
        self.booster = BoosterTasks()
        self.router = APIRouter(prefix="/api/v1", tags=["Create Actions"])
        self.router.add_api_route(
            path=self.path, 
            endpoint=self.create_action_with_photo,
            description="""Эндпоинт для "создания заявки" на буст. 
            принимает аргументы: \n
            - link - ссылка на объект,
            - action - действие, одно из [Likes, Comments],
            - type_action - тип объекта, один из [Photo, Reels]""",
            methods=["POST"], responses={
                200: {"model": ResponseSchema},
                400: {"model": ErrorSchema},
            }
        )

    async def create_action_with_photo(
        self, obj: CreatePhotoActionSchema, response: Response
    ):
        data = CreatePhotoActionSchema.model_validate(obj=obj)
        created = await self.orm.create_action(
            link=data.link, action=data.action, 
            type_action=data.type_action
        )
        if isinstance(created, str):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ErrorSchema(error=created)
        asyncio.create_task(
            self.booster.start_booster_action(action=created)
        )
        return ResponseSchema(response="Success")
    

class ActionsView:
    """View for Actions."""

    def __init__(self) -> None:
        self.path = "/actions/view/"
        self.orm = ActionsOrm()
        self.router = APIRouter(prefix="/api/v1", tags=["View Actions"])
        self.router.add_api_route(
            path=self.path, endpoint=self.get_action_by_state,
            description="""
            Эндпоинт для просмотра статусов заявок на буст. 
            принимает аргументы: \n
            - page - номер страницы(пагинация), 
            нумерация начинается с нуля,
            - state - состояние, одно из [done, in_progress, unactive],
            - type_action - тип объекта, один из [Photo, Reels]""",
            methods=["POST"], responses={
                200: {"model": ResponseActionsSchema},
                204: {"model": None},
            }
        )

    async def get_action_by_state(self, obj: RequestActionsSchema):
        data = RequestActionsSchema.model_validate(obj=obj)
        actions = await self.orm.get_actions_by_state(
            state=data.state, offset=data.page, 
            type_action=data.type_action
        )
        if not actions:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        result = []
        for action in actions:
            temp = ActionsSchema(
                state=data.state, action=action.action, 
                link=action.link, type_action=data.type_action
            )
            result.append(temp)
        return ResponseActionsSchema(page=data.page, actions=result)


create = CreateActionsView()
view = ActionsView()
