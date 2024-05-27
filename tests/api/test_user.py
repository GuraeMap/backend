from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from tests.conftest import test_app, test_db_session


def test_sign_up(test_app: TestClient, test_db_session: Session):

    # 정상 케이스
    response = test_app.post(
        "/v1/user/sign-up",
        json={
            "user_phone": "01012345678",
            "password": "password",
        },
    )
    assert response.json()["meta"]["code"] == 200

    test_db_session.execute(text("DELETE FROM user WHERE user_phone = '01012345678'"))
    test_db_session.commit()

    # 비정상 케이스

    response = test_app.post(
        "/v1/user/sign-up",
        json={
            "user_phone": "010123456781",
            "password": "password",
        },
    )
    assert response.status_code == 400


def test_sign_in(test_app: TestClient, test_db_session: Session):

    # 정상 케이스
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
    assert response.json()["meta"]["code"] == 200

    # # 비정상 케이스
    #
    # response = test_app.post(
    #     "/v1/user/sign-in",
    #     json={
    #         "user_phone": "01012345678",
    #         "password": "password1",
    #     },
    # )
    # assert response.json() == ""
    # assert response.json()["detail"]["meta"]["code"] == 400

    test_db_session.execute(text("DELETE FROM user WHERE user_phone = '01012345678'"))
    test_db_session.commit()


def test_sign_out(test_app: TestClient, test_db_session: Session):
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

    response = test_app.post(
        "/v1/user/sign-out",
        json={"access_token": f"Bearer {access_token}"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.json()["meta"]["code"] == 200

    test_db_session.execute(text("DELETE FROM user WHERE user_phone = '01012345678'"))
    test_db_session.commit()
