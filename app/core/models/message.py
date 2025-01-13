import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import func, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Role(Enum):
    admin = "user"
    lender = "system"


class Message(Base):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(backref="messages")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_winner: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    role: Mapped[Role] = mapped_column(nullable=True)
    tx_hash: Mapped[str] = mapped_column(Text, nullable=False)
    full_conversation: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"<Message[{self.id}], {self.content}, role {self.role}>"
