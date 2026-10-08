def test_register_and_login(client):
    """Test user registration flow followed by login."""
    # 1. Register new user
    res = client.post("/register", data={
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "secretpassword",
        "confirm_password": "secretpassword",
        "currency": "₹"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Welcome to PEIS" in res.data

    # 2. Logout
    res_logout = client.get("/logout", follow_redirects=True)
    assert res_logout.status_code == 200
    assert b"logged out" in res_logout.data

    # 3. Login again
    res_login = client.post("/login", data={
        "email": "alice@example.com",
        "password": "secretpassword"
    }, follow_redirects=True)
    assert res_login.status_code == 200
    assert b"Alice Smith" in res_login.data

def test_duplicate_registration(client):
    """Ensure duplicate email registration is rejected."""
    client.post("/register", data={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "password123",
        "confirm_password": "password123",
        "currency": "₹"
    })

    # Log out Bob before attempting duplicate registration
    client.get("/logout")

    res = client.post("/register", data={
        "name": "Bob Duplicate",
        "email": "bob@example.com",
        "password": "password123",
        "confirm_password": "password123",
        "currency": "₹"
    }, follow_redirects=True)
    assert b"already exists" in res.data

def test_invalid_login(client):
    """Ensure invalid credentials fail gracefully."""
    res = client.post("/login", data={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }, follow_redirects=True)
    assert b"Invalid email or password" in res.data
