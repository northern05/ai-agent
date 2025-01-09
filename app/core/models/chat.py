import datetime

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, State


class Chat(Base):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String(128), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    state: Mapped[State] = mapped_column(default=State.active, server_default=State.active.value)

    def __repr__(self):
        return f"<Chat[{self.id}] {self.uuid}>"