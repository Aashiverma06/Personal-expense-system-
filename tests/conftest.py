import os
import pytest
from app import create_app
from app.database import get_db, init_db
from app.models.user import User

TEST_DB_PATH = "/tmp/test_peis.db"

@pytest.fixture
def app():
    """Create application configured for testing."""
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass

    os.environ["FLASK_ENV"] = "testing"
    os.environ["DATABASE_PATH"] = TEST_DB_PATH

    app = create_app("testing")
    app.config["DATABASE_PATH"] = TEST_DB_PATH
    init_db(TEST_DB_PATH)

    yield app

    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass

@pytest.fixture
def client(app):
    """Test client fixture."""
    return app.test_client()

@pytest.fixture
def auth_client(client, app):
    """Test client with a pre-registered and logged-in user."""
    with app.app_context():
        user = User.create(
            name="Test User",
            email="test@peis.local",
            password="password123",
            currency="₹"
        )
    
    # Login session
    with client.session_transaction() as sess:
        sess["user_id"] = user.user_id

    return client, user
