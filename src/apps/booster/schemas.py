# Pydantic
from pydantic import BaseModel, Field

# Python
from typing import Literal, Union


class ActionSchema(BaseModel):
    """Schema for create action."""

    link: str = Field(...)
    action: Union[Literal["Likes"], Literal["Comments"], Literal["Views"]]
