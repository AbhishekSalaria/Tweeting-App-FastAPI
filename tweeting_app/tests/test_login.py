import pytest

@pytest.mark.parametrize("username, password, status_code",
                         [
    ("test_user","test_user",200),
    ("testuser","test_user",404),
    ("test_user","testuser",404),
                         ])
def test_login_user(client,test_user,username,password,status_code):
    response = client.post("/login/user",data = {"username":username,
                                                 "password":password})
    assert response.status_code == status_code