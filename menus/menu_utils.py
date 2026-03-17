### Utility functions for menu functions to be used in multiple menu files

# menu header function to display menu title and user information, with clear console for better readability
from database.user_db import user_status_fetch


def menu_header(title, user=None):
    # Clear the console (works on Windows and Unix-based systems)
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n================================")
    print("MES PRODUCTION SYSTEM")
    print("================================")

    # user variable name definitions for menu header display
    # Print user information in menu header if user data is provided
    if user is not None:
        username, role, user_number, employee_id = user
        print(f"User Name:    | {username}")
        print(f"Employee ID:  | {employee_id}")
        print(f"Role:         | {role}")
        print(f"User Status:  | {user_status_fetch(user_number)}")

    print("--------------------------------")
    print(title)
    print("--------------------------------")