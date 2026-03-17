from menus.menu_utils import menu_header
from database.user_db import user_update
from database.work_order_db import create_work_order, delete_work_order, edit_work_order, format_work_order_id, view_all_work_orders  
from menus.menu_work_order_management import menu_work_order_management
from menus.menu_workstation import menu_workstation

# choice 1 from main menu, to sign into work order, with options to view production data and update work order status, only available to users with role "user"
def menu_work_order(user_current):
    # workstations
    #assembly, software_installation, final_test =

    
    menu_header("WORK ORDER", user_current)
    work_order = input("Work Order: ")
    # user menu options within while loop
    while True:
        # Update user status to active and workstation to work order menu
        user_update(user_current, "idle", None)  # Update user status to active and workstation to work order menu
    
        # Display menu header 
        menu_header(f"WORK ORDER: {work_order}", user_current)
        print("1. Sign into Assembly")
        print("2. Sign into Software Installation")
        print("3. Sign into Final Test")
        print("4. View Work Order Information")
        print("0. Sign Out of Work Order and Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Signing into Assembly...")
            menu_workstation(work_order, "assembly", user_current)

        elif choice == "2":
            print("Signing into Software Installation...")
            menu_workstation(work_order, "software_installation", user_current)

        elif choice == "3":
            print("Signing into Final Test...")
            menu_workstation(work_order, "final_test", user_current)

        elif choice == "4":
            print("Viewing work order information...")
            

        elif choice == "0":
            break  # Exit the work order menu loop to return to main menu

        else:
            print("Invalid choice. Please try again.")



