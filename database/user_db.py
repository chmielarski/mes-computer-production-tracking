import sqlite3
from database.db import get_connection

### User management functions: create, edit, delete, identify, and status update
# User create function with auto-incrementing employee_number
def user_create(username, password, role, employee_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        print("Username already exists.")
        input("Press Enter to continue...") # user input requirement
        conn.close()
        return

    # Create employee_id if not exists
    if employee_id is None:
        cursor.execute("SELECT MAX(employee_id) FROM users")
        max_employee_id = cursor.fetchone()[0]
        employee_id = (max_employee_id or 400000000) + 1

    # Insert new user into the users database
    cursor.execute("""
        INSERT INTO users (username, password, role, user_status, employee_id)            
        VALUES (?, ?, ?, ?, ?)
        """, (username, password, role, 'offline', employee_id))
    print(f"User '{username}' created successfully with employee ID {employee_id}.")
    input("Press Enter to continue...") # user input requirement
    conn.commit()
    conn.close()

#user edit function, with options to edit username, password, role, and employee_id, with input validation for employee_id
def user_edit(user_number):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user is admin at user_number 1, if so, prevent deletion of admin user
    cursor.execute("SELECT user_number FROM users WHERE user_number = ?", (user_number,))
    row = cursor.fetchone()

    # admin edit prevention
    if row and row[0] == 1:
        print("Cannot edit admin user.")
        input("Press Enter to continue...")
        conn.close()
        return
    # optional: current user edit prevention.

    # Check if username exists
    cursor.execute("SELECT * FROM users WHERE user_number = ?", (user_number,))
    user = cursor.fetchone()
    if user is None:
        print("User does not exist.")
        input("Press Enter to continue...") # user input requirement
        conn.close()
        return

    # Get current user information
    current_username, current_password, current_role, current_user_status, current_employee_id = user[1], user[2], user[3], user[4], user[5]

    # Prompt for new information with current information as default
    new_username = input(f"Enter new username (current: {current_username}): ") or current_username
    new_password = input(f"Enter new password (current: {current_password}): ") or current_password
    new_role = input(f"Enter new role (current: {current_role}): ") or current_role
    
    # Employee ID input with validation
    while True:
        new_employee_id_input = input(f"Enter new employee ID (current: {current_employee_id}, leave blank to keep current): ")
        if new_employee_id_input == "":
            new_employee_id = current_employee_id
            break
        if new_employee_id_input.isdigit() and len(new_employee_id_input) == 9 and new_employee_id_input.startswith("400"):
            new_employee_id = int(new_employee_id_input)
            break
        print("Invalid employee ID. Employee ID must be a 9-digit number starting with '400'. Please try again.")

    # Update user information in the database
    cursor.execute("""
        UPDATE users SET username = ?, password = ?, role = ?, employee_id = ? WHERE user_number = ?
        """, (new_username, new_password, new_role, new_employee_id, user_number))
    print(f"User '{user_number}' updated successfully.")
    input("Press Enter to continue...") # user input requirement
    conn.commit()
    conn.close()

# User delete function
def user_delete(user_number):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user is admin at user_number 1, if so, prevent deletion of admin user
    cursor.execute("SELECT user_number FROM users WHERE user_number = ?", (user_number,))
    row = cursor.fetchone()
    # invalid input prevention
    if row is None:
        print("User does not exist.")
        input("Press Enter to continue...")
        conn.close()
        return

    # admin and current user deletion prevention
    if row and row[0] == 1:
        print("Cannot delete admin user.")
        input("Press Enter to continue...")
        conn.close()
        return
    
    if row == row[0]:
        print("Cannot delete current user.")
        input("Press Enter to continue...")
        conn.close()
        return

    # Check if username exists
    cursor.execute("SELECT * FROM users WHERE user_number = ?", (user_number,))
    if cursor.fetchone() is None:
        print("User does not exist.")
        input("Press Enter to continue...") # user input requirement
        conn.close()
        return

    # Delete user from the users database
    cursor.execute("DELETE FROM users WHERE user_number = ?", (user_number,))
    print(f"User '{user_number}' deleted successfully.")
    input("Press Enter to continue...") # user input requirement
    conn.commit()
    conn.close()
# function to toggle account status between enabled and disabled, with disabled users unable to log in 
def user_toggle_account_status(user_number):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT account_status FROM users WHERE user_number = ?", (user_number,))
    row = cursor.fetchone()
    if row is None:
        print("User does not exist.")
        input("Press Enter to continue...") # user input requirement
        conn.close()
        return

    current_status = row[0]
    new_status = "disabled" if current_status == "enabled" else "enabled"

    cursor.execute("""
        UPDATE users SET account_status = ? WHERE user_number = ?
        """, (new_status, user_number))
    print(f"User '{user_number}' account status updated to '{new_status}'.")
    input("Press Enter to continue...") # user input requirement
    conn.commit()
    conn.close()

# User identification function
def user_identify(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE username = ? AND password = ?
        """, (username, password))
    user = cursor.fetchone()
    conn.close()
    #if user exists, return user
    if user is not None:
        return user
    return None

# User status update function
def user_update(user_current, user_status, workstation_name=None):
    username, role, user_number, employee_id = user_current
    conn = get_connection()
    cursor = conn.cursor()


    # change user status to status_id based on status_name input
    cursor.execute("""
        UPDATE users SET user_status = ? WHERE user_number = ?
        """, (user_status, user_number))
    conn.commit()

    # change user workstation to workstation_name input
    if workstation_name is not None:
        cursor.execute("""
            UPDATE users SET user_workstation = ? WHERE user_number = ?
            """, (workstation_name, user_number))
        conn.commit()

    else: # if workstation_name is None, set user workstation to None
        cursor.execute("""
            UPDATE users SET user_workstation = NULL WHERE user_number = ?
            """, (user_number,))
        conn.commit()

    conn.close()

def user_status_fetch(user_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_status FROM users WHERE user_number = ?
        """, (user_number,))
    user_status = cursor.fetchone()
    conn.close()
    if user_status is not None:
        return user_status[0]
    return None

def user_workstation_fetch(user_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_workstation FROM users WHERE user_number = ? 
        """, (user_number,))
    user_workstation = cursor.fetchone()
    conn.close()
    if user_workstation is not None:
        return user_workstation[0]
    return None

# users table fetch function
def users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return users