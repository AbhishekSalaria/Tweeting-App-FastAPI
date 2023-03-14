import pytest

def test_register_user(client):
    response = client.post("/register/user",json={"username":"test_user",
                                                  "email":"test_user@gmail.com",
                                                  "password":"test_user",
                                                  "is_active": False,
                                                  "is_superuser": False
                                                })

    assert response.status_code == 201

@pytest.mark.parametrize("username, email, password, is_active, is_superuser",
                        [
    ("test_user","test_user@gmail.com","test_user",False,False),
    ("test_user","test_user123@gmail.com","test_user",False,False),
    ("test_user123","test_user@gmail.com","test_user",False,False),
                        ] )
def test_check_duplicate_user(client,test_user,username,email,password,is_active,is_superuser):
    response = client.post("/register/user",json={"username":username,
                                                  "email":email,
                                                  "password":password,
                                                  "is_active": is_active,
                                                  "is_superuser": is_superuser
                                                })

    assert response.status_code == 409
