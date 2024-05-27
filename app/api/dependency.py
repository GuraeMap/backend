from datetime import datetime, timedelta

import jwt
from typing import Literal, Annotated

from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

from app.api.common.dto.base_response_dto import BaseResponseMeta, BaseResponseDTO
from app.config.config import default
from app.config.redis_config import redis_session


class AuthHandler:
    def __call__(self, req: Request):
        token = req.headers.get("Authorization", None)

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authorization header is required",
            )

        _, token = token.split("Bearer ")

        payload = self.decode_token(token)

        return payload

    def encode_token(self, id, type: Literal["access", "refresh"]):

        if type == "access":
            token_exp = datetime.utcnow() + timedelta(hours=1)

        else:
            token_exp = datetime.utcnow() + timedelta(days=1)

        payload = {
            "exp": token_exp,
            "iat": datetime.utcnow(),
            "token_type": type,
            "id": id,
        }
        return jwt.encode(payload, default.JWT_SECRET_KEY, algorithm="HS256")

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, default.JWT_SECRET_KEY, algorithms="HS256")

        except jwt.ExpiredSignatureError:
            refresh_token = redis_session.get(f"user_refresh_token:{token}")
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=BaseResponseDTO(
                        meta=BaseResponseMeta(
                            code=status.HTTP_400_BAD_REQUEST,
                            message="Expired token",
                            data=None,
                        )
                    ).model_dump_json(),
                )
            payload = jwt.decode(
                refresh_token, default.JWT_SECRET_KEY, algorithms="HS256"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BaseResponseDTO(
                    meta=BaseResponseMeta(
                        code=status.HTTP_400_BAD_REQUEST,
                        message="Invalid token",
                        data=None,
                    )
                ).model_dump_json(),
            )
        return payload


auth_handler = AuthHandler()


##
user = Annotated[dict, Depends(auth_handler)]
