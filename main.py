import sqlite3
from database.db import initialize_database
from auth import login
from database.user_db import user_update
from menus.menu_main import menu_main, menu_header
from database.user_statuses_db import get_user_status_map

def main():
    # Initialize the database and create tables if they don't exist
    initialize_database()

    statuses = get_user_status_map()

    while True:
        # Menu header
        menu_header("LOGIN")
        # Start the authentication process
        user_current = login()

        # if user exists call menu function with user data as argument to display user information and options based on role
        if user_current:
            menu_main(user_current)
            user_update((user_current), statuses["offline"], None)  # Update user status to offline when user logs out
    
if __name__ == "__main__":
    main()

