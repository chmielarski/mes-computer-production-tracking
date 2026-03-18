from menus.menu_utils import menu_header
from database.user_db import user_create, user_delete, user_edit, user_toggle_account_status, users_table

# does not need a status update -- nothing changes at this level
# choice 2 from main menu, only available to admin users, to manage users in the system, with options to create, edit, and delete users
def menu_user_manager(user_current):
    
    # user menu options within while loop
    while True:
        
        # Display menu header 
        menu_header("MANAGE USERS", user_current)
        print("1. Create User")
        print("2. Edit User")
        print("3. Toggle Account Status (enabled/disabled)") # optional feature to disable user accounts without deleting them, with disabled users unable to log in
        print("4. Delete User")
        print("5. View Users Table") # optional feature to display users table for reference when managing users
        print("0. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1": # create user
            # code to create user here
            username_new = input("Enter new username: ")
            password_new = input("Enter new password: ")
            role_new = input("Enter new user role (admin/user): ")
            
            # verify employee_id validity, auto generation available if left blank
            while True:
                employee_id_new = input("Enter new employee ID (leave blank for auto-generation): ")
                if employee_id_new == "":
                    employee_id_new = None
                    break
                if employee_id_new.isdigit() and len(employee_id_new) == 9 and employee_id_new.startswith("400"):
                    employee_id_new = int(employee_id_new)
                    break
                print("Invalid employee ID. Employee ID must be a 9-digit number starting with '400'. Please try again.")
            
            user_create(username_new, password_new, role_new, employee_id_new)
            print(f"User '{username_new}' created successfully with employee ID {employee_id_new}.") # user created confirmation
                
        
        elif choice == "2": # edit user
            menu_header("EDIT USER", user_current)
            # Display users table with username, employee_id, and role for reference when editing users
            print(f"{'USER #':<10} | {'USERNAME':<20} | {'EMPLOYEE ID':<15} | {'ROLE':<10}")
            for user in users_table():
                print(f"{user[0]:<10} | {user[1]:<20} | {user[7]:<15} | {user[3]:<10}")
            
            #username input for user to edit, with user_edit function call to edit user information in database, with input validation for employee_id
            user_number = input("Enter the user number of the user to edit: ")
            user_edit(user_number)

        elif choice == "3": # toggle account status
            menu_header("TOGGLE ACCOUNT STATUS", user_current)
            # Display users table with username, employee_id, role, and account status for reference when toggling account status
            print(f"{'USER #':<10} | {'USERNAME':<20} | {'EMPLOYEE ID':<15} | {'ROLE':<10} | {'ACCOUNT STATUS':<15}")
            for user in users_table():
                print(f"{user[0]:<10} | {user[1]:<20} | {user[7]:<15} | {user[3]:<10} | {user[6]:<15}")
            
            user_number = input("Enter the user number of the user to toggle account status: ")
            user_toggle_account_status(user_number) # function to toggle account status between enabled and disabled, with disabled users unable to log in 
           
        elif choice == "4": # delete user
            menu_header("DELETE USER", user_current)
            # Display users table with username, employee_id, and role for reference when editing users
            print(f"{'USER #':<10} | {'USERNAME':<20} | {'EMPLOYEE ID':<15} | {'ROLE':<10}")
            for user in users_table():
                print(f"{user[0]:<10} | {user[1]:<20} | {user[7]:<15} | {user[3]:<10}")
            
            user_number = input("Enter the user number of the user to delete: ")
            user_delete(user_number)
        
        elif choice == "5": # optional feature to display users table for reference
            menu_header("USERS TABLE", user_current)
            print(f"{'USER #':<10} | {'USERNAME':<20} | {'EMPLOYEE ID':<15} | {'ROLE':<10} | {'ACCOUNT STATUS':<15}")
            for user in users_table():
                print(f"{user[0]:<10} | {user[1]:<20} | {user[7]:<15} | {user[3]:<10} | {user[6]:<15}")
            input("Press Enter to continue...") # user input requirement to return to manage users menu after viewing users table
            
        elif choice == "0": #
            break  # Exit the manage users menu loop to return to main menu
        else:
            print("Invalid choice. Please try again.")