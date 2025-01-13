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


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exec_logs: str | None = None
    body: str
    decision: str
    timestamp: int


class DataIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    context_data: dict | None = None
    message: str
    timestamp: int
    transaction_hash: str
    wallet_address: str
