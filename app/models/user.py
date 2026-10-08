from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

class User:
    """User model managing authentication and profile data."""

    def __init__(self, user_id, name, email, password_hash, currency='₹', created_at=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.currency = currency
        self.created_at = created_at

    @classmethod
    def create(cls, name, email, password, currency='₹'):
        """Registers a new user with hashed password."""
        hashed = generate_password_hash(password)
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash, currency) VALUES (?, ?, ?, ?)",
                (name.strip(), email.strip().lower(), hashed, currency)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return cls.get_by_id(user_id)
        except Exception:
            conn.rollback()
            return None
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, user_id):
        """Fetches user record by ID."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["user_id"], row["name"], row["email"], row["password_hash"], row["currency"], row["created_at"])
        return None

    @classmethod
    def get_by_email(cls, email):
        """Fetches user record by email."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["user_id"], row["name"], row["email"], row["password_hash"], row["currency"], row["created_at"])
        return None

    @classmethod
    def authenticate(cls, email, password):
        """Validates login credentials."""
        user = cls.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    def update_profile(self, name=None, currency=None):
        """Updates user profile information."""
        conn = get_db()
        cursor = conn.cursor()
        if name:
            self.name = name.strip()
        if currency:
            self.currency = currency
        cursor.execute(
            "UPDATE users SET name = ?, currency = ? WHERE user_id = ?",
            (self.name, self.currency, self.user_id)
        )
        conn.commit()
        conn.close()
        return True

    def change_password(self, new_password):
        """Updates user's password securely."""
        new_hash = generate_password_hash(new_password)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE user_id = ?",
            (new_hash, self.user_id)
        )
        conn.commit()
        conn.close()
        self.password_hash = new_hash
        return True
