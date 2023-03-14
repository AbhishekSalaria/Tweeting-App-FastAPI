def test_get_all_tweets_of_all_users(test_tweet,authorized_client):
    response = authorized_client.get("/tweets/get/all/users")

    assert response.status_code == 200

def test_get_all_tweets_of_all_users_failure(client):
    response = client.get("/tweets/get/all/users")

    assert response.status_code == 401

def test_get_all_tweets_of_single_user(test_tweet,authorized_client):
    response = authorized_client.get("/tweets/get/all/user/1")

    assert response.status_code == 200

def test_get_all_tweets_of_single_user_failure(client):
    response = client.get("/tweets/get/all/user/1")

    assert response.status_code == 401   

def test_get_all_users(authorized_client):
    response = authorized_client.get("/get/all/users")

    assert response.status_code == 200       

def test_get_all_users_failure(client):
    response = client.get("/get/all/users")

    assert response.status_code == 401      

def test_get_active_users(authorized_client):
    response = authorized_client.get("/get/active/users")

    assert response.status_code == 200           

def test_get_active_users_failure(client):
    response = client.get("/get/active/users")

    assert response.status_code == 401

def test_get_inactive_users(authorized_client):
    response = authorized_client.get("/get/inactive/users")

    assert response.status_code == 200     

def test_get_inactive_users(client):
    response = client.get("/get/inactive/users")

    assert response.status_code == 401         

def test_delete_any_tweet(test_tweet, authorized_client):
    response = authorized_client.delete("/tweet/delete/users/1")

    assert response.status_code == 200          

def test_delete_any_tweet_failure(client):
    response = client.delete("/tweet/delete/users/1")

    assert response.status_code == 401          

def test_delete_user(test_tweet,authorized_client):
    response = authorized_client.delete("/account/delete/user/1")

    assert response.status_code == 200        

def test_delete_user_failure(client):
    response = client.delete("/account/delete/user/1")

    assert response.status_code == 401   

def test_make_user_active(authorized_client):
    response = authorized_client.put("/account/active/user/1")

    assert response.status_code == 200   

def test_make_user_active_failure(client):
    response = client.put("/account/active/user/1")

    assert response.status_code == 401           

def test_make_user_inactive(authorized_client):
    response = authorized_client.put("/account/inactive/user/1")

    assert response.status_code == 200  

def test_make_user_inactive_failure(client):
    response = client.put("/account/inactive/user/1")

    assert response.status_code == 401        