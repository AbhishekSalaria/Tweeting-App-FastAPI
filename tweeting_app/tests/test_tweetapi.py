def test_post_new_tweet(authorized_client):
    response = authorized_client.post("/tweet/post/user",
                                      json = {"tweet":"Test Tweet"})
    assert response.status_code == 200

def test_post_new_tweet_failure(client):
    response = client.post("/tweet/post/user",
                           json = {"tweet":"Test Tweet"})
    assert response.status_code == 401

def test_get_all_tweets(test_tweet,authorized_client):
    response = authorized_client.get("/tweet/get/user")
    data = response.json()
    assert data[0].get("id") == 1
    assert response.status_code == 200

def test_get_all_tweets_failure(client):
    response = client.get("/tweet/get/user")
    assert response.status_code == 401    

def test_edit_tweet(test_tweet,authorized_client):
    response = authorized_client.put("/tweet/edit/user/1",
                                     json = {"tweet":"Edit Success"})
    assert response.status_code == 200

def test_edit_tweet_failure(client):
    response = client.put("/tweet/edit/user/1",
                          json = {"tweet":"Edit Success"})
    assert response.status_code == 401

def test_delete_user_tweet(test_tweet,authorized_client):
    response = authorized_client.delete("/tweet/delete/user/1")
    assert response.status_code == 200

def test_delete_user_tweet_failure(client):
    response = client.delete("/tweet/delete/user/1")
    assert response.status_code == 401