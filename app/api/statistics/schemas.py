from pydantic import BaseModel

class MessageCountResponse(BaseModel):
    total_messages: int

class UsersCountResponse(BaseModel):
    total_users: int