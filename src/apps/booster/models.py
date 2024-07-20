# SQLAlchemy
import sqlalchemy as sa

# Local
from src.apps.abstract.models import Base


class Actions(Base):
    """Model for Actions."""

    __tablename__ = "actions"

    id = sa.Column(sa.BigInteger, primary_key=True, unique=True)
    link = sa.Column(sa.Text, index=True)
    action = sa.Column(sa.String, index=True)
    is_done = sa.Column(sa.Boolean, default=False)

    def __repr__(self) -> str:
        return (f"<Actions(id={self.id}, link={self.link}, "
                f"action={self.action}, done={self.is_done}>")
    