# Pydantic
from pydantic import BaseModel, Field


class BotSchema(BaseModel):
    """Schema for view/create bot."""

    username: str = Field(min_length=6, max_length=50)
    password: str = Field(min_length=6, max_length=50)


class BotsSchema(BaseModel):
    """Schema for view all bots."""
    
    page: int = Field(ge=0)
    bots: list[BotSchema]
