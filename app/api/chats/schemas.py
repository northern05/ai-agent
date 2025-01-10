import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.core.models.base import State


class ChatBase(BaseModel):
    name: str | None = None
    uuid: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    pass


class ChatUpdatePartial(ChatBase):
    name: str | None = None
    uuid: None = None


class ChatSchema(ChatBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    state: State
    user_id: int


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exec_logs: str | None = None
    body: str
    decision: str
    timestamp: int


class StrategyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExtendedChatSchema(ChatSchema):
    model_config = ConfigDict(from_attributes=True)

    history: list = []


class DataIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    context_data: dict | None = None
    message: str
    timestamp: int
    msg_hash: str