from database.user_db import user_identify, user_status_update

# Authentication module for MES Computer Production Tracking System
def login():
    # Loop until user successfully logs in
    while True:
        username = input("Username: ")
        password = input("Password: ")

        user = user_identify(username, password)
        
        # Check if user exists and credentials are correct
        if user is None:
            print("Invalid username or password. Please try again.")
            continue
        else:   # Unpack critical information
            (
            user_number_db,
            username_db,
            password_db,
            role_db,
            user_status_db,
            user_workstation_db,
            account_status_db,   
            employee_id_db
            ) = user

        # Verify credentials
        if username_db == username and password_db == password:
            user_status_update(user_number_db, "idle")  # Update user status to idle
            user_data_return = username_db, role_db, user_number_db, employee_id_db  # Return username, role, user_number, employee_id
            return user_data_return
        else:   # if credentials are incorrect, prompt user to try again, while loops
            print("Invalid username or password. Please try again.")

    
    

    

