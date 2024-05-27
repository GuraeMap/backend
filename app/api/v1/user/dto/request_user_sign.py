import re
from pydantic import BaseModel, field_validator
from starlette import status
from fastapi.responses import JSONResponse

from app.api.common.dto.base_response_dto import BaseResponseDTO, BaseResponseMeta
from fastapi.exceptions import HTTPException


class RequestUserSignUpDTO(BaseModel):
    user_phone: str
    password: str

    @field_validator("user_phone")
    @classmethod
    def validate_phone(cls, v):
        is_valid_phone = bool(re.match(r"^\d{11}$", v))
        if not is_valid_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BaseResponseDTO(
                    meta=BaseResponseMeta(
                        code=status.HTTP_400_BAD_REQUEST,
                        message="Invalid phone number",
                        data=None,
                    )
                ).model_dump_json(),
            )
        return v
