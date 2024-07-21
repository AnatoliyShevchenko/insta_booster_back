# Pydantic
from pydantic import BaseModel, Field

# Python
from typing import Literal


class CreatePhotoActionSchema(BaseModel):
    """Schema for create action for photo."""

    link: str = Field(...)
    action: Literal["Likes", "Comments"] = Field(...)
    type_action: Literal["Photo", "Reels"] = Field(...)


class RequestActionsSchema(BaseModel):
    """Request Schema for view Actions."""

    page: int = Field(ge=0)
    state: Literal["done", "in_progress", "unactive"] = Field(...)
    type_action: Literal["Photo", "Reels"] = Field(...)


class ActionsSchema(BaseModel):
    """Schema for Actions."""

    state: Literal["done", "in_progress", "unactive"] = Field(...)
    action: Literal["Likes", "Comments", "View"] = Field(...)
    type_action: Literal["Photo", "Reels"] = Field(...)
    link: str = Field(...)


class ResponseActionsSchema(BaseModel):
    """Response Schema for actions."""

    page: int = Field(ge=0)
    actions: list[ActionsSchema]
