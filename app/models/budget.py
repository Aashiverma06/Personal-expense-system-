from app.database import get_db

class Budget:
    """Budget model managing monthly category allowances and tracking."""

    @classmethod
    def set_budget(cls, user_id, category, amount, month, year):
        """Creates or updates a monthly category budget."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO budgets (user_id, category, amount, month, year)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(user_id, category, month, year)
               DO UPDATE SET amount = excluded.amount""",
            (user_id, category, float(amount), int(month), int(year))
        )
        conn.commit()
        b_id = cursor.lastrowid
        conn.close()
        return b_id

    @classmethod
    def delete_budget(cls, budget_id, user_id):
        """Deletes a budget entry."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM budgets WHERE budget_id = ? AND user_id = ?",
            (budget_id, user_id)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    @classmethod
    def get_budgets_with_spending(cls, user_id, month, year):
        """
        Retrieves all budgets for the given month/year and joins actual spending,
        computing utilization percentage, remaining allowance, and risk status.
        """
        conn = get_db()
        cursor = conn.cursor()

        # Month string pattern (e.g. '2026-10-%')
        date_pattern = f"{year:04d}-{month:02d}-%"

        query = """
            SELECT 
                b.budget_id,
                b.category,
                b.amount AS budget_amount,
                b.month,
                b.year,
                COALESCE(SUM(t.amount), 0.0) AS spent_amount
            FROM budgets b
            LEFT JOIN transactions t 
                ON t.user_id = b.user_id 
                AND t.category = b.category 
                AND t.type = 'expense'
                AND t.date LIKE ?
            WHERE b.user_id = ? AND b.month = ? AND b.year = ?
            GROUP BY b.budget_id, b.category, b.amount, b.month, b.year
            ORDER BY b.category ASC
        """
        cursor.execute(query, (date_pattern, user_id, month, year))
        rows = cursor.fetchall()
        conn.close()

        results = []
        for r in rows:
            b_amt = float(r["budget_amount"])
            spent = float(r["spent_amount"])
            remaining = b_amt - spent
            pct = round((spent / b_amt * 100), 1) if b_amt > 0 else 0.0

            if pct > 100:
                status = "exceeded"
                badge_class = "danger"
            elif pct >= 80:
                status = "warning"
                badge_class = "warning"
            else:
                status = "safe"
                badge_class = "success"

            results.append({
                "budget_id": r["budget_id"],
                "category": r["category"],
                "budget_amount": round(b_amt, 2),
                "spent_amount": round(spent, 2),
                "remaining_amount": round(remaining, 2),
                "percentage_used": pct,
                "status": status,
                "badge_class": badge_class,
                "month": r["month"],
                "year": r["year"]
            })

        return results
