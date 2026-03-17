import sqlite3
import datetime

### Database functions
DB_NAME = "mes_database.db"
# Database connection function
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

# Database initialization and user management functions
def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        user_number INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        user_status TEXT DEFAULT 'offline', 
        user_workstation TEXT DEFAULT 'none',
        account_status TEXT DEFAULT 'enabled',   
        employee_id INTEGER UNIQUE NOT NULL    
        )  
    """)
    conn.commit()

    # Create admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (user_number, username, password, role, employee_id) VALUES (?, ?, ?, ?, ?)
        """, ("1", "admin", "admin123", "admin", 400000000))
        conn.commit()

    # Create work_orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        created_by TEXT NOT NULL,
        date_created TEXT NOT NULL,
        status STRING NOT NULL DEFAULT ''
        )
    """) 
    conn.commit()

    # Create work_orders_statuses table, with options for not started, in progress, and completed
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_orders_statuses (
        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status_name TEXT NOT NULL UNIQUE
        )
    """)

    # insert work_orders_statuses if not exists
    cursor.execute("SELECT * FROM work_orders_statuses")
    if cursor.fetchone() is None:
        work_orders_statuses = [
            ("Not Started",),
            ("In Progress",),
            ("Completed",)
        ]
        cursor.executemany("""
            INSERT INTO work_orders_statuses (status_name) VALUES (?)
        """, work_orders_statuses)
        conn.commit()


    # workstations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workstations (
        workstation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        workstation_name TEXT NOT NULL UNIQUE,
        sequence_order INTEGER NOT NULL
        )
    """)
    conn.commit()

    # insert workstations if not exists
    cursor.execute("SELECT * FROM workstations")
    if cursor.fetchone() is None:
        workstations = [
            ("Assembly", 1), 
            ("Software Installation", 2), 
            ("Final Test", 3)
        ]
        cursor.executemany("""
            INSERT INTO workstations (workstation_name, sequence_order) VALUES (?, ?)
        """, workstations)
        conn.commit()

    # user statuses table, with options for offline, idle, and active
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_statuses (
        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status_name TEXT NOT NULL UNIQUE
        )
    """)

    # insert user statuses if not exists
    cursor.execute("SELECT * FROM user_statuses")
    if cursor.fetchone() is None:
        user_statuses = [
            ("Offline",), 
            ("Idle",), 
            ("Active",)
        ]
        cursor.executemany("""
            INSERT INTO user_statuses (status_name) VALUES (?)
        """, user_statuses)
        conn.commit()

    # account statuses table, with options for enabled and disabled
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_statuses (
        account_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_status_name TEXT NOT NULL UNIQUE
        )
    """)

    # insert account statuses if not exists
    cursor.execute("SELECT * FROM account_statuses")
    if cursor.fetchone() is None:
        account_statuses = [
            ("Enabled",),
            ("Disabled",)
        ]
        cursor.executemany("""
            INSERT INTO account_statuses (account_status_name) VALUES (?)
        """, account_statuses)
        conn.commit()
    
    # workstation sessions table, to track user sign in and sign out times at each workstation, with foreign keys to users and work orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workstation_sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        work_order_number INTEGER NOT NULL,
        user_number INTEGER NOT NULL,
        workstation_id INTEGER NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        labour_hours REAL,
        status INTEGER
       )
    """)

    conn.commit()

    conn.close()



