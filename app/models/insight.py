from app.database import get_db

class Insight:
    """Model for storing and managing generated insights."""

    @classmethod
    def get_user_insights(cls, user_id, active_only=True):
        """Fetches insights for a user."""
        conn = get_db()
        cursor = conn.cursor()
        if active_only:
            cursor.execute(
                "SELECT * FROM insights WHERE user_id = ? AND is_dismissed = 0 ORDER BY created_at DESC LIMIT 10",
                (user_id,)
            )
        else:
            cursor.execute(
                "SELECT * FROM insights WHERE user_id = ? ORDER BY created_at DESC LIMIT 20",
                (user_id,)
            )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @classmethod
    def dismiss(cls, insight_id, user_id):
        """Marks an insight as dismissed."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE insights SET is_dismissed = 1 WHERE insight_id = ? AND user_id = ?",
            (insight_id, user_id)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
