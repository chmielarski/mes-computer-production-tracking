from database.user_db import user_create, user_delete, user_edit, user_status_update, users_table
from database.work_order_db import create_work_order
from menus.menu_user_management import menu_user_manager
from menus.menu_work_order import menu_work_order, menu_work_order_management
from menus.menu_utils import menu_header
        
# main menu function, with user as input to sign on and edit sqlite users
def menu_main(user_current):
    # user variable name definitions for menu header display
    username, role, user_number, employee_id = user_current
    
    # user menu options within while loop
    while True:
        # Display menu header 
        menu_header("MAIN MENU", user_current)

        # user menu options here, while loop to keep user in menu until they choose to log out, which breaks the loop and returns to login screen
        print("1. Enter Work Order")

        # admin menu options within while loop
        if role == "admin":
           print("2. Manage Users")
           print("3. View Reports")
           print("4. Manage Work Orders")

        # logout  
        print("0. Log Out")
        # user input for menu options
        choice = input("Enter your choice: ")
    
        # handle user choice for menu navigation
        if choice == "1":
            menu_work_order(user_current)

        elif choice == "2" and role == "admin":
            menu_user_manager(user_current)
        
        elif choice == "3" and role == "admin":
            print("Viewing reports...")
            # code to view reports here
        elif choice == "4" and role == "admin":
            print("Managing work orders...")
            menu_work_order_management(user_current)

        elif choice == "0":
            print("Logging out...")
            user_status_update(user_number, "offline")  # Update user status to offline using user_number
            break  # Exit the menu loop to return to login screen

        else:
            print("Invalid choice. Please try again.")




