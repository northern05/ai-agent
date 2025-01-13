import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User

class Message(Base):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(backref="messages")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    decision: Mapped[bool] = mapped_column(String(8), nullable=False, server_default="reject")

    def __repr__(self):
        return f"<Message[{self.id}], {self.content}>"
