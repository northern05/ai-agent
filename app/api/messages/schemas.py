from typing import Optional
import datetime
from pydantic import BaseModel, ConfigDict

from app.core.models.message import Role

class MessageBase(BaseModel):
    id: int
    user_id: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageSchema(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime.datetime
    user_id: int
    is_winner: bool
    role: Role
    content: Optional[str] = None
    tx_hash: Optional[str] = None
    full_conversation: Optional[str] = None
    wallet: Optional[str] = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exec_logs: str | None = None
    body: str
    decision: str
    timestamp: int


class DataIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
    timestamp: int
    transaction_hash: str
