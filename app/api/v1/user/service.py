import bcrypt

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from starlette import status

from app.api.common.dto.base_response_dto import BaseResponseDTO, BaseResponseMeta
from app.api.dependency import auth_handler
from app.api.v1.user.dto.request_user_sign import RequestUserSignUpDTO
from app.api.v1.user.dto.request_user_sign_dto import RequestUserSigninDTO
from app.api.v1.user.dto.request_user_sign_out_dto import RequestUserSignOutDTO

from app.api.v1.user.entity.user import User
from app.api.v1.user.utils import PasswordBcrypt
from app.config.redis_config import redis_session


def post_user_signup(db_session: Session, data: RequestUserSignUpDTO):
    if (
        is_phone_check := db_session.execute(
            select(User).filter(User.user_phone == data.user_phone)
        ).scalar_one_or_none()
    ) is not None:
        return BaseResponseDTO(
            meta=BaseResponseMeta(
                code=status.HTTP_400_BAD_REQUEST, message="Phone already", data=None
            )
        )

    data.password = PasswordBcrypt.generate_password_hash(data.password)

    db_session.execute(
        insert(User).values(
            user_phone=data.user_phone,
            password=data.password,
        )
    )
    db_session.commit()

    return BaseResponseDTO(
        meta=BaseResponseMeta(code=status.HTTP_200_OK, message="ok", data=None)
    )


def post_user_signin(
    db_session: Session,
    data: RequestUserSigninDTO,
):
    if (
        user_data := db_session.execute(
            select(User).filter(User.user_phone == data.user_phone)
        ).scalar_one_or_none()
    ) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=BaseResponseDTO(
                meta=BaseResponseMeta(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Phone does not exist",
                    data=None,
                )
            ).model_dump_json(),
        )

    is_verified = PasswordBcrypt.check_password_hash(data.password, user_data.password)

    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=BaseResponseDTO(
                meta=BaseResponseMeta(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Password is incorrect",
                    data=None,
                )
            ).model_dump_json(),
        )
    access_token = auth_handler.encode_token(user_data.id, "access")
    redis_session.set(
        f"user_refresh_token:{access_token}",
        auth_handler.encode_token(user_data.id, "refresh"),
        60 * 60 * 2,
    )
    return BaseResponseDTO(
        meta=BaseResponseMeta(
            code=status.HTTP_200_OK, message="ok", data={"access_token": access_token}
        )
    )


def post_user_sign_out(user, data: RequestUserSignOutDTO):
    redis_session.delete(f"user_refresh_token:{data.access_token}")
    return BaseResponseDTO(
        meta=BaseResponseMeta(code=status.HTTP_200_OK, message="ok", data=True)
    )
