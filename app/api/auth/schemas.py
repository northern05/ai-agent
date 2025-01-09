from pydantic import ConfigDict, BaseModel


class AuthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    refresh_token: str
