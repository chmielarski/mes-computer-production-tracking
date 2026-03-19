import sqlite3

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
        work_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        work_order_number TEXT UNIQUE,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        created_by TEXT NOT NULL,
        date_created TEXT NOT NULL,
        status STRING NOT NULL DEFAULT ''
        )
    """) 
    conn.commit()
    
    # check if work_orders table is empty
    cursor.execute("SELECT * FROM work_orders")
    if cursor.fetchone() is None:

        default_work_orders = [
            ("WO-0001", "Test Product", 10, "system", "2026-01-01 00:00:00", 1)
        ]

        cursor.executemany("""
            INSERT INTO work_orders (
                work_order_number,
                product_name,
                quantity,
                created_by,
                date_created,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, default_work_orders)

        conn.commit()
        
    # Create work_orders_statuses table, with options for not started, in progress, and completed
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_order_statuses (
        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status_name TEXT NOT NULL UNIQUE
        )
    """)

    # insert work_orders_statuses if not exists
    cursor.execute("SELECT * FROM work_order_statuses")
    if cursor.fetchone() is None:
        work_order_statuses = [
            ("not started",),
            ("in progress",),
            ("complete",)
        ]
        cursor.executemany("""
            INSERT INTO work_order_statuses (status_name) VALUES (?)
        """, work_order_statuses)
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
            ("assembly", 1), 
            ("software installation", 2), 
            ("final test", 3)
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
            ("offline",), 
            ("idle",), 
            ("active",)
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
        work_order_id INTEGER NOT NULL,
        user_number INTEGER NOT NULL,
        workstation_id INTEGER NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        labour_minutes INTEGER,
        is_handoff INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    # create test workstation session if workstation_sessions table is empty
    cursor.execute("SELECT * FROM workstation_sessions")
    if cursor.fetchone() is None:
        cursor.execute("""
        INSERT INTO workstation_sessions (work_order_id, user_number, workstation_id, start_time, end_time, labour_minutes, is_handoff)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (1, 400000000, 1, "2026-03-18 08:00:00", "2026-03-18 10:00:00", 120, 0))
        conn.commit()
    

    # create checklist table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checklists (
        checklist_id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_type_id, INTEGER NOT NULL,
        workstation_id INTEGER NOT NULL,
        is_completed INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    
    conn.close()
    



