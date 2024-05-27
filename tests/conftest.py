import pytest
import sys
import pathlib
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config.config import default
from app.main import app

url = default.db_url
engine = create_engine(url)


@pytest.fixture(scope="session")
def test_db_session():
    sess = Session(bind=engine)

    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client
