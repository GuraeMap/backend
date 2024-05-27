from pydantic import BaseModel


class RequestUserSignOutDTO(BaseModel):
    access_token: str
