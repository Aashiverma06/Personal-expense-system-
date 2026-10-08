from app.database import get_db

class Category:
    """Category model representing income and expense classifications."""

    @classmethod
    def get_all(cls, user_id=None, cat_type=None):
        """Fetches all system categories plus custom user categories."""
        conn = get_db()
        cursor = conn.cursor()
        
        query = "SELECT * FROM categories WHERE (user_id IS NULL"
        params = []
        if user_id:
            query += " OR user_id = ?"
            params.append(user_id)
        query += ")"

        if cat_type:
            query += " AND type = ?"
            params.append(cat_type)

        query += " ORDER BY name ASC"
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @classmethod
    def create(cls, name, cat_type, user_id=None, icon='tag', color='#3b82f6'):
        """Creates a custom category."""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO categories (name, type, user_id, icon, color)
                   VALUES (?, ?, ?, ?, ?)""",
                (name.strip(), cat_type, user_id, icon, color)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception:
            conn.rollback()
            return None
        finally:
            conn.close()
