from fastapi import APIRouter

from app.api.v1.user import service
from app.api.v1.user.dto.request_user_sign import RequestUserSignUpDTO
from app.api.v1.user.dto.request_user_sign_dto import RequestUserSigninDTO
from app.api.v1.user.dto.request_user_sign_out_dto import RequestUserSignOutDTO
from app.config.db.database import DbSession
from app.api.dependency import user

api = APIRouter(prefix="/user", tags=["user"])


@api.post(
    "/sign-up",
    response_description="""
    <H1> 회원 가입 Post </H1>
    """,
)
def post_user_signup(db_session: DbSession, data: RequestUserSignUpDTO):
    return service.post_user_signup(db_session, data)


@api.post(
    "/sign-in",
    response_description="""
    <H1> 로그인 Post </H1>
    """,
)
def post_user_signin(db_session: DbSession, data: RequestUserSigninDTO):
    return service.post_user_signin(db_session, data)


@api.post(
    "/sign-out",
    response_description="""
    <H1> 로그아웃 Post </H1>
    
    """,
)
def post_user_signout(user: user, data: RequestUserSignOutDTO):
    return service.post_user_sign_out(user, data)
