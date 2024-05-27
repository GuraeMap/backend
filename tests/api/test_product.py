import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from tests.conftest import test_app, test_db_session


# 유저 생성 -> 테스트 -> 유저 삭제


@pytest.fixture(scope="module")
def user_token(test_app, test_db_session):
    response = test_app.post(
        "/v1/user/sign-up",
        json={
            "user_phone": "01012345678",
            "password": "password",
        },
    )

    response = test_app.post(
        "/v1/user/sign-in",
        json={
            "user_phone": "01012345678",
            "password": "password",
        },
    )

    access_token = response.json()["meta"]["data"]["access_token"]
    yield access_token
    test_db_session.execute(text("DELETE FROM user WHERE user_phone = '01012345678'"))
    test_db_session.commit()

def test_create_product(
    test_app: TestClient, test_db_session: Session, user_token: str
):
    product_data = {
        "id": 1,
        "category": "커피",
        "selling_price": 1000,
        "cost_price": 500,
        "name": "슈크림 라떼",
        "description": "A지점 달고 달디난 라떼",
        "barcode": "random-string",
        "expiration_date": "2024-05-06",
        "size": "large",
        "search_keywords": "슈크림,크림,라떼,ㅅㅋㄹ,ㄹㄸ",
    }

    response = test_app.post(
        "/v1/product/",
        headers={"Authorization": f"Bearer {user_token}"},
        json=product_data,
    )
sponse = test_app.post(
        "/v1/user/sign-up",
        json={
            "user_phone": "01012345678",
            "password": "password",
        },
    )

    response = test_app.post(
        "/v1/user/sign-in",
        json={
            "user_phone": "01012345678",
            "password": "password",
        },
    )

    access_token = response.json()["meta"]["data"]["access_token"]
    yield access_token
    test_db_session.execute(text("DELETE FROM user WHERE user_phone = '01012345678'"))
    test_db_session.commit()

    assert response.json()["meta"]["code"] == 201


def test_find_user_product_detail(
    test_app: TestClient, test_db_session: Session, user_token: str
):
    response = test_app.get(
        f"/v1/product/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.json()["meta"]["code"] == 200


def test_update_user_product(
    test_app: TestClient, test_db_session: Session, user_token: str
):

    response = test_app.put(
        f"/v1/product/1",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "카라멜 라떼"},
    )

    assert response.json()["meta"]["code"] == 200


def test_find_user_product_search(
    test_app: TestClient, test_db_session: Session, user_token: str
):

    product_data = {
        "id": 2,
        "category": "커피",
        "selling_price": 1000,
        "cost_price": 500,
        "name": "카라멜 라떼",
        "description": "B지점 달고 달디난 라떼",
        "barcode": "random-string",
        "expiration_date": "2024-05-06",
        "size": "large",
        "search_keywords": "카라멜,라떼,ㄹㄸ",
    }

    response = test_app.post(
        "/v1/product/",
        headers={"Authorization": f"Bearer {user_token}"},
        json = product_data,
    )

    response = test_app.get(
        "/v1/product/search?search_keyword=ㄹㄸ",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert len(response.json()["meta"]["data"]) == 2






def test_find_user_product_list (test_app : TestClient, test_db_session : Session, user_token : str):

    # 정상 케이스
    response = test_app.get(
        "/v1/product/?current_page=1",
        headers={"Authorization": f"Bearer {user_token}"}
    )


    assert len(response.json()["meta"]["data"]) == 2

    response = test_app.get(
        "/v1/product/?current_page=2",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    
    assert len(response.json()["meta"]["data"]) == 0



def test_delete_product(test_app : TestClient, test_db_session : Session, user_token : str):


    response = test_app.delete(
        f"/v1/product/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.json()["meta"]["code"] == 200

    response = test_app.delete(
        f"/v1/product/2",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.json()["meta"]["code"] == 200