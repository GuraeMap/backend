from typing import Any, Optional
from pydantic import BaseModel


class BaseResponseMeta(BaseModel):
    code: int
    message: str
    data: Optional[Any]


class BaseResponseDTO(BaseModel):
    meta: BaseResponseMeta
