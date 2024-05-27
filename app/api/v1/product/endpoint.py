from typing import Optional, Literal, Annotated

from fastapi import APIRouter, Query, Path

from app.api.v1.product import service
from app.api.v1.product.dto.request_update_user_product import RequestUpdateUserProduct
from app.api.v1.product.dto.request_user_product import RequestUserProduct
from app.config.db.database import DbSession

from app.api.dependency import user

api = APIRouter(prefix="/product", tags=["product"])


@api.get("")
def find_user_product_list(
    user: user,
    db_session: DbSession,
    current_page: Optional[int] = Query(1, description="current_page"),
):
    return service.find_user_product_list(user, db_session, current_page)


@api.post(
    "",
)
def create_user_product(user: user, db_session: DbSession, data: RequestUserProduct):
    return service.create_user_product(user, db_session, data)


@api.get("/search")
def find_user_product_search(
    user: user,
    db_session: DbSession,
    search_keyword: str = Query(description="검색 키워드"),
):
    return service.find_user_product_search(user, db_session, search_keyword)


@api.delete(
    "/{product_id}",
)
def delete_user_product(
    user: user,
    db_session: DbSession,
    product_id: int = Path(..., description="product_id"),
):
    return service.delete_user_product(user, db_session, product_id)


@api.get(
    "/{product_id}",
)
def find_user_product_detail(
    user: user,
    db_session: DbSession,
    product_id: int = Path(..., description="product_id"),
):
    return service.find_user_product_detail(user, db_session, product_id)


@api.put(
    "/{product_id}",
)
def update_user_product(
    user: user,
    db_session: DbSession,
    data: RequestUpdateUserProduct,
    product_id: int = Path(..., description="product_id"),
):
    return service.update_user_product(user, db_session, product_id, data)
