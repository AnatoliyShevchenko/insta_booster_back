# SQLAlchemy
import sqlalchemy as sa

# Local
from src.apps.abstract.models import Base


class Bots(Base):
    """Model for bots."""

    __tablename__ = "bots"

    id = sa.Column(
        sa.BigInteger, primary_key=True, unique=True
    )
    username = sa.Column(
        sa.String, nullable=False, index=True
    )
    password = sa.Column(sa.String, nullable=False)

    def __repr__(self):
        return f"<Bots(id={self.id}, username={self.username})>"
