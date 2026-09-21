import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('amazon.db')
cursor = conn.cursor()

# -----------------------------
# STEP 1: CREATE TABLES
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    city TEXT,
    join_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# -----------------------------
# STEP 2: DUMMY DATA
# -----------------------------

random.seed(42)

# ---------- CUSTOMERS ----------
first_names = [
    "Rajib", "Aman", "Rahul", "Rohan", "Arjun",
    "Vikash", "Amit", "Ankit", "Karan", "Aditya",
    "Neha", "Priya", "Sneha", "Pooja", "Anjali"
]

last_names = [
    "Kumar", "Sharma", "Singh", "Patel", "Verma",
    "Gupta", "Das", "Jain", "Mishra", "Roy"
]

cities = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Bhubaneswar",
    "Jaipur",
    "Ahmedabad"
]

customers = []

start_date = datetime(2023, 1, 1)

for i in range(120):

    name = random.choice(first_names) + " " + random.choice(last_names)

    email = (
        name.lower()
        .replace(" ", ".")
        + str(i + 1)
        + "@gmail.com"
    )

    city = random.choice(cities)

    join_date = (
        start_date +
        timedelta(days=random.randint(0, 1000))
    ).strftime("%Y-%m-%d")

    customers.append(
        (name, email, city, join_date)
    )

cursor.executemany("""
INSERT INTO customers
(name, email, city, join_date)
VALUES (?, ?, ?, ?)
""", customers)


# ---------- PRODUCTS ----------

product_data = [
    ("Laptop", "Electronics", 55000),
    ("Smartphone", "Electronics", 25000),
    ("Headphones", "Electronics", 2500),
    ("Keyboard", "Electronics", 1500),
    ("Mouse", "Electronics", 800),
    ("Monitor", "Electronics", 12000),
    ("Smart Watch", "Electronics", 5000),
    ("Power Bank", "Electronics", 1800),
    ("USB Cable", "Electronics", 500),
    ("Bluetooth Speaker", "Electronics", 3000),

    ("T-Shirt", "Clothing", 799),
    ("Jeans", "Clothing", 1499),
    ("Jacket", "Clothing", 2499),
    ("Shoes", "Clothing", 2999),
    ("Shirt", "Clothing", 1299),
    ("Sweatshirt", "Clothing", 1999),
    ("Track Pants", "Clothing", 999),
    ("Saree", "Clothing", 2499),
    ("Cap", "Clothing", 499),
    ("Socks", "Clothing", 299),

    ("Backpack", "Accessories", 1499),
    ("Wallet", "Accessories", 799),
    ("Belt", "Accessories", 699),
    ("Sunglasses", "Accessories", 1299),
    ("Watch", "Accessories", 3499),

    ("Python Book", "Books", 699),
    ("Data Science Book", "Books", 899),
    ("Machine Learning Book", "Books", 999),
    ("SQL Book", "Books", 599),
    ("Java Book", "Books", 799),

    ("Coffee Maker", "Home", 4500),
    ("Electric Kettle", "Home", 1800),
    ("Table Lamp", "Home", 1200),
    ("Bedsheet", "Home", 999),
    ("Pillow", "Home", 599),
    ("Water Bottle", "Home", 499),
    ("Cookware Set", "Home", 3500),
    ("Vacuum Cleaner", "Home", 8500),
    ("Chair", "Home", 5000),
    ("Study Table", "Home", 7000)
]

cursor.executemany("""
INSERT INTO products
(name, category, price)
VALUES (?, ?, ?)
""", product_data)


# ---------- ORDERS ----------

orders = []

order_start_date = datetime(2024, 1, 1)

for i in range(130):

    customer_id = random.randint(1, 120)

    order_date = (
        order_start_date +
        timedelta(days=random.randint(0, 900))
    ).strftime("%Y-%m-%d")

    # temporary amount
    total_amount = 0

    orders.append(
        (customer_id, order_date, total_amount)
    )

cursor.executemany("""
INSERT INTO orders
(customer_id, order_date, total_amount)
VALUES (?, ?, ?)
""", orders)


# ---------- ORDER ITEMS ----------

order_items = []

# Get all products
cursor.execute("""
SELECT product_id, price
FROM products
""")

products = cursor.fetchall()

# Create 1-4 items for each order
for order_id in range(1, 131):

    number_of_items = random.randint(1, 4)

    selected_products = random.sample(
        products,
        number_of_items
    )

    total_amount = 0

    for product_id, price in selected_products:

        quantity = random.randint(1, 5)

        subtotal = price * quantity

        total_amount += subtotal

        order_items.append(
            (
                order_id,
                product_id,
                quantity,
                subtotal
            )
        )

    # Update order total
    cursor.execute("""
    UPDATE orders
    SET total_amount = ?
    WHERE order_id = ?
    """, (total_amount, order_id))


cursor.executemany("""
INSERT INTO order_items
(order_id, product_id, quantity, subtotal)
VALUES (?, ?, ?, ?)
""", order_items)


# -----------------------------
# STEP 3: SAVE CHANGES
# -----------------------------

conn.commit()

print("Dummy data inserted successfully!")

# -----------------------------
# STEP 4: CHECK ROW COUNTS
# -----------------------------

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table}: {count} rows")


conn.close()