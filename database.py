import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            items TEXT,
            total INTEGER,
            order_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_order(customer_name, items, total, order_date):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (customer_name, items, total, order_date) VALUES (?, ?, ?, ?)",
        (customer_name, items, total, order_date)
    )
    conn.commit()
    conn.close()

def get_all_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    conn.close()
    return orders
