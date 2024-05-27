from pydantic import BaseModel


class RequestUserSigninDTO(BaseModel):
    user_phone: str
    password: str
