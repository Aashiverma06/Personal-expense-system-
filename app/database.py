import sqlite3
import os
from datetime import datetime, timedelta
import random
from flask import has_app_context, current_app
from app.config import Config
from app.data.default_dataset import DEFAULT_CATEGORIES

def get_db(db_path=None):
    """Obtain a SQLite database connection with row factory enabled."""
    if db_path is None:
        if has_app_context() and "DATABASE_PATH" in current_app.config:
            db_path = current_app.config["DATABASE_PATH"]
        else:
            db_path = os.environ.get("DATABASE_PATH", Config.DATABASE_PATH)
    
    # Ensure directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(db_path=None):
    """Initialize database tables and seed default categories."""
    conn = get_db(db_path)
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        currency TEXT DEFAULT '₹',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
        icon TEXT DEFAULT 'tag',
        color TEXT DEFAULT '#3b82f6',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        UNIQUE(name, user_id)
    )
    """)

    # 3. Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
        amount REAL NOT NULL CHECK(amount > 0),
        category TEXT NOT NULL,
        description TEXT,
        payment_method TEXT NOT NULL,
        date TEXT NOT NULL,
        is_auto_categorized INTEGER DEFAULT 0,
        categorization_method TEXT DEFAULT 'manual',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """)

    # 4. Budgets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount > 0),
        month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12),
        year INTEGER NOT NULL CHECK(year > 2000),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, category, month, year),
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """)

    # 5. Insights table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insights (
        insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        severity TEXT DEFAULT 'info',
        is_dismissed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """)

    # Create helpful indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_trans_user_date ON transactions(user_id, date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_trans_category ON transactions(user_id, category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_budgets_lookup ON budgets(user_id, year, month)")

    # Seed default system categories if empty
    cursor.execute("SELECT COUNT(*) AS count FROM categories WHERE user_id IS NULL")
    count = cursor.fetchone()["count"]
    if count == 0:
        for cat in DEFAULT_CATEGORIES:
            cursor.execute(
                "INSERT INTO categories (user_id, name, type, icon, color) VALUES (NULL, ?, ?, ?, ?)",
                (cat["name"], cat["type"], cat.get("icon", "tag"), cat.get("color", "#3b82f6"))
            )

    conn.commit()
    conn.close()

def seed_demo_data(user_id, db_path=None):
    """
    Seeds rich, realistic transactions across the current and previous month
    for immediate demonstration of PEIS charts, budgets, and intelligence insights.
    """
    conn = get_db(db_path)
    cursor = conn.cursor()

    # Check if user already has transactions
    cursor.execute("SELECT COUNT(*) as count FROM transactions WHERE user_id = ?", (user_id,))
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return False

    today = datetime.now()
    curr_year = today.year
    curr_month = today.month

    # Previous month
    if curr_month == 1:
        prev_month = 12
        prev_year = curr_year - 1
    else:
        prev_month = curr_month - 1
        prev_year = curr_year

    # 1. Seed Budgets for current month
    default_budgets = [
        ("Food & Dining", 6500.0),
        ("Transportation", 2500.0),
        ("Entertainment", 2000.0),
        ("Shopping", 4000.0),
        ("Housing & Utilities", 12000.0),
        ("Education", 3000.0)
    ]
    for cat, amt in default_budgets:
        cursor.execute(
            """INSERT OR REPLACE INTO budgets (user_id, category, amount, month, year)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, cat, amt, curr_month, curr_year)
        )

    # 2. Seed Transactions for Previous Month (baseline)
    prev_transactions = [
        ("income", 45000.0, "Salary", "Monthly Corporate Salary Transfer", "Bank Transfer", f"{prev_year}-{prev_month:02d}-01"),
        ("expense", 11000.0, "Housing & Utilities", "Apartment rent to landlord", "Bank Transfer", f"{prev_year}-{prev_month:02d}-02"),
        ("expense", 1450.0, "Housing & Utilities", "Electricity power board bill", "UPI", f"{prev_year}-{prev_month:02d}-05"),
        ("expense", 999.0, "Housing & Utilities", "Airtel broadband fiber wifi", "UPI", f"{prev_year}-{prev_month:02d}-07"),
        ("expense", 1200.0, "Food & Dining", "Weekly supermarket groceries", "Debit Card", f"{prev_year}-{prev_month:02d}-08"),
        ("expense", 450.0, "Food & Dining", "Domino's pizza delivery dinner", "UPI", f"{prev_year}-{prev_month:02d}-10"),
        ("expense", 320.0, "Transportation", "Uber cab to office campus", "UPI", f"{prev_year}-{prev_month:02d}-12"),
        ("expense", 800.0, "Transportation", "Petrol fuel refill for bike", "Cash", f"{prev_year}-{prev_month:02d}-14"),
        ("expense", 650.0, "Entertainment", "PVR Cinemas movie tickets", "Credit Card", f"{prev_year}-{prev_month:02d}-15"),
        ("expense", 199.0, "Entertainment", "Spotify premium music subscription", "Debit Card", f"{prev_year}-{prev_month:02d}-16"),
        ("expense", 1800.0, "Shopping", "Puma casual sneakers Flipkart", "Credit Card", f"{prev_year}-{prev_month:02d}-18"),
        ("expense", 1500.0, "Education", "Python Data Science certification Udemy", "Credit Card", f"{prev_year}-{prev_month:02d}-20"),
        ("expense", 480.0, "Healthcare", "Doctor consultation and cough syrup", "Cash", f"{prev_year}-{prev_month:02d}-22"),
        ("expense", 1650.0, "Food & Dining", "Family weekend buffet dinner", "UPI", f"{prev_year}-{prev_month:02d}-25"),
        ("income", 5000.0, "Freelance", "Freelance web design milestone", "Bank Transfer", f"{prev_year}-{prev_month:02d}-27")
    ]

    for t_type, amt, cat, desc, method, t_date in prev_transactions:
        cursor.execute(
            """INSERT INTO transactions 
               (user_id, type, amount, category, description, payment_method, date, is_auto_categorized, categorization_method)
               VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'ml')""",
            (user_id, t_type, amt, cat, desc, method, t_date)
        )

    # 3. Seed Transactions for Current Month (including an exceeded entertainment budget and high shopping for intelligence triggers)
    curr_day = min(today.day, 28)
    day_str = lambda d: f"{curr_year}-{curr_month:02d}-{min(d, curr_day):02d}"

    curr_transactions = [
        ("income", 48000.0, "Salary", "Monthly Corporate Salary Paycheck", "Bank Transfer", day_str(1)),
        ("expense", 11000.0, "Housing & Utilities", "Monthly apartment flat house rent", "Bank Transfer", day_str(2)),
        ("expense", 1620.0, "Housing & Utilities", "State electricity power bill", "UPI", day_str(4)),
        ("expense", 999.0, "Housing & Utilities", "Fiber broadband wifi recharge", "UPI", day_str(5)),
        ("expense", 1850.0, "Food & Dining", "Supermarket organic vegetables & groceries", "UPI", day_str(6)),
        ("expense", 720.0, "Food & Dining", "Swiggy biryani dinner delivery", "UPI", day_str(8)),
        ("expense", 540.0, "Food & Dining", "Starbucks cold coffee & bagels", "Debit Card", day_str(10)),
        ("expense", 1250.0, "Transportation", "Petrol fuel refill at Shell pump", "Credit Card", day_str(11)),
        ("expense", 480.0, "Transportation", "Uber cab ride to tech park", "UPI", day_str(12)),
        ("expense", 320.0, "Transportation", "Metro train smartcard recharge", "UPI", day_str(13)),
        ("expense", 1450.0, "Entertainment", "IMAX 3D Movie tickets BookMyShow", "Credit Card", day_str(14)),
        ("expense", 799.0, "Entertainment", "Netflix 4K Ultra subscription", "Credit Card", day_str(15)),  # Exceeds budget 2000!
        ("expense", 2400.0, "Shopping", "Zara formal shirts and trousers", "Credit Card", day_str(16)),
        ("expense", 1899.0, "Shopping", "Amazon wireless Bluetooth earbuds", "Credit Card", day_str(18)),  # High shopping spend
        ("expense", 650.0, "Healthcare", "Apollo Pharmacy vitamin supplements", "Debit Card", day_str(20)),
        ("expense", 450.0, "Personal Care", "Haircut and styling salon barber", "Cash", day_str(21)),
        ("expense", 2200.0, "Education", "Coursera Deep Learning specialization", "Credit Card", day_str(22)),
        ("income", 7500.0, "Freelance", "Client frontend mobile app consulting", "Bank Transfer", day_str(24))
    ]

    for t_type, amt, cat, desc, method, t_date in curr_transactions:
        cursor.execute(
            """INSERT INTO transactions 
               (user_id, type, amount, category, description, payment_method, date, is_auto_categorized, categorization_method)
               VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'ml')""",
            (user_id, t_type, amt, cat, desc, method, t_date)
        )

    conn.commit()
    conn.close()
    return True
