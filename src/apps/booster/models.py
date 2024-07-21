# SQLAlchemy
import sqlalchemy as sa

# Python
from dataclasses import dataclass

# Local
from src.apps.abstract.models import Base


class Actions(Base):
    """Model for Actions."""

    __tablename__ = "actions"

    id = sa.Column(sa.BigInteger, primary_key=True, unique=True)
    link = sa.Column(sa.Text, index=True)
    action = sa.Column(sa.String, index=True)
    type_action = sa.Column(sa.String, index=True)
    is_done = sa.Column(sa.Boolean, default=False)
    in_progress = sa.Column(sa.Boolean, default=False)

    def __str__(self) -> str:
        return (f"<Actions(id={self.id}, link={self.link}, "
            f"action={self.action}, type_action={self.type_action}, "
            f"done={self.is_done}, in_progress={self.in_progress}>")
    

@dataclass
class ActionData:
    id: int
    link: str
    action: str
    type_action: str
