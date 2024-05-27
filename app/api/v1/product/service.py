from sqlalchemy import select, update
from sqlalchemy.orm import Session
from fastapi import status

from app.api.common.dto.base_response_dto import BaseResponseMeta, BaseResponseDTO
from app.api.dependency import user
from app.api.v1.product.dto.request_update_user_product import RequestUpdateUserProduct
from app.api.v1.product.dto.request_user_product import RequestUserProduct
from app.api.v1.product.dto.response_user_product_list import (
    ResponseUserProductList,
    ResponseUserProductListDTO,
)
from app.api.v1.product.entity.product import Product
from app.api.v1.user.entity.user import User


def find_user_product_list(user: user, db_session: Session, current_page: int):
    user_product_data = (
        db_session.execute(
            select(Product)
            .filter(Product.user_id == user["id"])
            .offset((current_page - 1) * 10)
            .limit(10)
        )
        .scalars()
        .all()
    )

    return ResponseUserProductListDTO(
        meta=BaseResponseMeta(
            code=status.HTTP_200_OK,
            message="ok",
            data=[
                ResponseUserProductList.model_validate(data)
                for data in user_product_data
            ],
        ),
    )


def create_user_product(user: user, db_session: Session, data: RequestUserProduct):
    data.user_id = user["id"]
    data.search_keywords = "".join(
        [f"{str(ord(i))}_" if not i == "," else "," for i in data.search_keywords]
    ).replace("_,", ",")[:-1]
    data = data.model_dump(exclude_none=True)

    data = Product(**data)
    db_session.add(data)
    try:
        db_session.commit()
    except Exception as e:
        print(e)
        return BaseResponseDTO(
            meta=BaseResponseMeta(
                code=status.HTTP_400_BAD_REQUEST,
                message=e,
                data=None,
            )
        )
    return BaseResponseDTO(
        meta=BaseResponseMeta(code=status.HTTP_201_CREATED, message="ok", data=None)
    )


def delete_user_product(user: user, db_session: Session, product_id: int):
    delete_product_data = db_session.get(Product, product_id)
    if not delete_product_data.user_id == user["id"]:
        return BaseResponseDTO(
            meta=BaseResponseMeta(
                code=status.HTTP_400_BAD_REQUEST, message="Invalid user", data=None
            )
        )
    db_session.delete(delete_product_data)
    try:
        db_session.commit()
    except Exception as e:
        return BaseResponseDTO(
            meta=BaseResponseMeta(
                code=status.HTTP_400_BAD_REQUEST, message=e, data=None
            )
        )
    return BaseResponseDTO(
        meta=BaseResponseMeta(code=status.HTTP_200_OK, message="ok", data=None)
    )


def find_user_product_detail(user: user, db_session: Session, product_id: int):
    find_product_data = db_session.get(Product, product_id)
    if not find_product_data.user_id == user["id"]:
        return BaseResponseDTO(
            meta=BaseResponseMeta(
                code=status.HTTP_400_BAD_REQUEST, message="Invalid user", data=None
            )
        )
    return BaseResponseDTO(
        meta=BaseResponseMeta(
            code=status.HTTP_200_OK,
            message="ok",
            data=ResponseUserProductList.model_validate(find_product_data),
        )
    )


def update_user_product(
    user: user,
    db_session: Session,
    product_id: int,
    data: RequestUpdateUserProduct,
):
    data = data.model_dump(exclude_none=True)
    find_product_data = db_session.get(Product, product_id)

    if not find_product_data.user_id == user["id"]:
        return BaseResponseDTO(
            meta=BaseResponseMeta(
                code=status.HTTP_400_BAD_REQUEST, message="Invalid user", data=None
            )
        )

    try:
        db_session.execute(
            update(Product)
            .filter(Product.id == product_id)
            .filter(Product.user_id == user["id"])
            .values(**data)
        )
        db_session.commit()
    except Exception as e:
        return BaseResponseDTO(
            meta=BaseResponseMeta(code=status.HTTP_400_BAD_REQUEST, message=e, data = None)
        )
    return BaseResponseDTO(
        meta=BaseResponseMeta(code=status.HTTP_200_OK, message="ok", data=None)
    )


def find_user_product_search(user: user, db_session: Session, search_keyword: str):
    search_keyword = "_".join([str(ord(i)) for i in search_keyword])
    search_product_data = (
        db_session.execute(
            select(Product)
            .filter(Product.user_id == user["id"])
            .filter(Product.search_keywords.match(search_keyword))
        )
        .scalars()
        .all()
    )

    return BaseResponseDTO(
        meta=BaseResponseMeta(
            code=status.HTTP_200_OK,
            message="ok",
            data=[
                ResponseUserProductList.model_validate(data)
                for data in search_product_data
            ],
        )
    )
