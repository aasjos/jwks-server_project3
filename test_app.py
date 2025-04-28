def test_register(client):
    response = client.post('/register', json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code in (200, 201)

def test_auth(client):
    response = client.post('/auth', json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code in (400, 401)
