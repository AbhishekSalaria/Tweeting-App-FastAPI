import sys
sys.path.append("..")

from fastapi.testclient import TestClient
from tweeting_app.main import app
from tweeting_app.routers.auth.register import User
from tweeting_app.routers.auth.login import get_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tweeting_app.database.database import Base,get_db
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/testapp.db"

engine = create_engine (
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()        

@pytest.fixture
def client(session):
  def override_get_db():
    try:
        yield session
    finally:
        session.close()
  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)

@pytest.fixture
def test_user(client):
    payload = {"username":"test_user",
               "email":"test_user@gmail.com",
               "password":"test_user",
               "is_active": True,
               "is_superuser": True}
    response = client.post("/register/user",json=payload)

    assert response.status_code == 201
    return {"username":payload["username"],"user_id":1}

@pytest.fixture
def token(test_user):
    return get_access_token(test_user["username"],test_user["user_id"])

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_tweet(authorized_client):
    response = authorized_client.post("/tweet/post/user",
                                      json = {"tweet":"Test Tweet"})
    assert response.status_code == 200