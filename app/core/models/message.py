import datetime

from sqlalchemy import func, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Message(Base):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    decision: Mapped[bool] = mapped_column(String(8), nullable=False, server_default="reject")

    def __repr__(self):
        return f"<Message[{self.id}], {self.content}>"
