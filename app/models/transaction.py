import io
import csv
from datetime import datetime
from app.database import get_db

class Transaction:
    """Transaction model supporting CRUD, flexible querying, and export."""

    @classmethod
    def create(cls, user_id, t_type, amount, category, description, 
               payment_method, date, is_auto_categorized=0, categorization_method='manual'):
        """Inserts a new transaction record."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO transactions 
               (user_id, type, amount, category, description, payment_method, date, is_auto_categorized, categorization_method)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, t_type, float(amount), category, description, payment_method, date, is_auto_categorized, categorization_method)
        )
        conn.commit()
        t_id = cursor.lastrowid
        conn.close()
        return t_id

    @classmethod
    def get_by_id(cls, transaction_id, user_id):
        """Retrieves a single transaction by ID verifying user ownership."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM transactions WHERE transaction_id = ? AND user_id = ?",
            (transaction_id, user_id)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @classmethod
    def update(cls, transaction_id, user_id, t_type=None, amount=None, category=None,
               description=None, payment_method=None, date=None):
        """Updates an existing transaction."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE transactions
               SET type = COALESCE(?, type),
                   amount = COALESCE(?, amount),
                   category = COALESCE(?, category),
                   description = COALESCE(?, description),
                   payment_method = COALESCE(?, payment_method),
                   date = COALESCE(?, date)
               WHERE transaction_id = ? AND user_id = ?""",
            (t_type, amount, category, description, payment_method, date, transaction_id, user_id)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    @classmethod
    def delete(cls, transaction_id, user_id):
        """Deletes a transaction by ID."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM transactions WHERE transaction_id = ? AND user_id = ?",
            (transaction_id, user_id)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    @classmethod
    def search(cls, user_id, start_date=None, end_date=None, t_type=None, 
               category=None, payment_method=None, query=None, limit=None, offset=None):
        """
        Advanced transaction search with multi-field filtering and pagination.
        """
        conn = get_db()
        cursor = conn.cursor()

        sql = ["SELECT * FROM transactions WHERE user_id = ?"]
        params = [user_id]

        if start_date:
            sql.append("AND date >= ?")
            params.append(start_date)
        if end_date:
            sql.append("AND date <= ?")
            params.append(end_date)
        if t_type and t_type != "all":
            sql.append("AND type = ?")
            params.append(t_type)
        if category and category != "all":
            sql.append("AND category = ?")
            params.append(category)
        if payment_method and payment_method != "all":
            sql.append("AND payment_method = ?")
            params.append(payment_method)
        if query:
            sql.append("AND (description LIKE ? OR category LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])

        sql.append("ORDER BY date DESC, transaction_id DESC")

        if limit:
            sql.append("LIMIT ?")
            params.append(int(limit))
            if offset:
                sql.append("OFFSET ?")
                params.append(int(offset))

        cursor.execute(" ".join(sql), tuple(params))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def export_csv(transactions):
        """Generates a CSV formatted string from transaction list."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Date", "Type", "Category", "Amount", "Payment Method", "Description", "Categorization Method"])
        for t in transactions:
            writer.writerow([
                t.get("transaction_id", ""),
                t.get("date", ""),
                t.get("type", "").capitalize(),
                t.get("category", ""),
                f"{t.get('amount', 0):.2f}",
                t.get("payment_method", ""),
                t.get("description", ""),
                t.get("categorization_method", "manual")
            ])
        return output.getvalue()
