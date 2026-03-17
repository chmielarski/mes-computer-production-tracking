import sqlite3
from datetime import datetime
from database.db import get_connection

### Work order management functions: create, edit, delete, and identify
# work order creation function, with inputs for product name, quantity, and created by, with auto-incrementing order number and date created
def create_work_order(user_current):
    conn = get_connection()
    cursor = conn.cursor()

    # Get user input for product name and quantity, and use username from user_current tuple for created_by field
    product_name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    created_by = user_current[1] # Get username from user_current tuple
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "not started"

    cursor.execute("""
        INSERT INTO work_orders (product_name, quantity, created_by, date_created, status) VALUES (?, ?, ?, ?, ?)
    """, (product_name, quantity, created_by, date_created, status))
    conn.commit()
    print(f"Work order for {quantity} {product_name}(s) created successfully.")
    input("Press Enter to continue...") # user input requirement
    
    wo_id = cursor.lastrowid

    order_number = f"WO-{wo_id:04d}"

    cursor.execute("""
    UPDATE work_orders
    SET order_number = ?
    WHERE id = ?
    """, (order_number, wo_id))
    conn.commit()
    conn.close()

# work order edit function, with input as order_number, userinput is product_name, quantity
def edit_work_order(id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if work order exists
    cursor.execute("SELECT * FROM work_orders WHERE id = ?", (id,))
    work_order = cursor.fetchone()
    order_number = work_order[1]

    if work_order is None:
        print("Work order does not exist.")
        input("Press Enter to continue...") # user input requirement
        conn.close()
        return

    # Get new values for product name, quantity, and status
    product_name = input("Enter new product name: ")
    quantity = int(input("Enter new quantity: "))
    status = int(input("Enter new status (0 for in progress, 1 for completed): "))

    cursor.execute("""
        UPDATE work_orders SET product_name = ?, quantity = ?, status = ? WHERE id = ?
    """, (product_name, quantity, status, id))
    conn.commit()
    print(f"Work order {order_number} updated successfully.")
    input("Press Enter to continue...") # user input requirement
    conn.close()

# delete selected work order function, with input as order_number
def delete_work_order(id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if work order exists
    cursor.execute("SELECT * FROM work_orders WHERE id = ?", (id,))
    work_order = cursor.fetchone()
    order_number = work_order[1]
    if work_order is None:
        print("Work order does not exist.")
        input("Press Enter to continue...") # user input requirement
        conn.close()
        return

    cursor.execute("DELETE FROM work_orders WHERE order_number = ?", (order_number,))
    conn.commit()
    print(f"Work order {order_number} deleted successfully.")
    input("Press Enter to continue...") # user input requirement
    conn.close()

# view all work orders function, returns list of all work orders in database
def view_all_work_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM work_orders")
    work_orders = cursor.fetchall()
    conn.close()
    return work_orders

def get_all_workstations():

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workstations ORDER BY sequence_order")
    workstations = cursor.fetchall()
    conn.close()
    return workstations

def format_work_order_id(wo_id):
    return f"WO-{wo_id:04d}"