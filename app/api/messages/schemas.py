from typing import Optional
import datetime
from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    id: int
    user_id: str
    decision: str
    response: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageSchema(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime.datetime
    user_id: int
    decision: str
    response: str
    content: str
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
    wallet_address: str
