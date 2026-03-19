from menus.menu_utils import menu_header
from database.user_db import user_update
from menus.menu_workstation import menu_workstation
from database.user_statuses_db import get_user_status_map
from database.workstations_db import get_workstation_map
from database.work_order_db import get_work_order

# choice 1 from main menu, to sign into work order, with options to view production data and update work order status, only available to users with role "user"
def menu_work_order(user_current):
    
    # workstations
    workstations = get_workstation_map()
    statuses = get_user_status_map()

    # work order header
    menu_header("WORK ORDER", user_current)
    
    work_order = get_work_order_table()
    if work_order is None:
        
        return
    # user menu options within while loop
    while True:
        
        # Update user status to active and workstation to work order menu
        user_update(user_current, statuses["idle"], None)  # Update user status to active and workstation to work order menu
    
        # Display menu header 
        menu_header(f"WORK ORDER: {work_order[1]}", user_current)
        print("1. Sign into Assembly")
        print("2. Sign into Software Installation")
        print("3. Sign into Final Test")
        print("4. View Work Order Information")
        print("0. Sign Out of Work Order and Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1": ## sign into assembly workstation
            menu_workstation(work_order, workstations["assembly"], user_current)

        elif choice == "2": ## sign into software installation workstation
            menu_workstation(work_order, workstations["software installation"], user_current)
        
        elif choice == "3": ## sign into final test workstation
            menu_workstation(work_order, workstations["final test"], user_current)

        elif choice == "4": ## view work order information
            print("Viewing work order information...")
            

        elif choice == "0":
            break  # Exit the work order menu loop to return to main menu

        else:
            print("Invalid choice. Please try again.")

# work order table at input int xxxx function
def get_work_order_table():
    while True:
        
        # work order input detection
        order_number_input = input("Work Order: WO-")
        if len(order_number_input) < 4:
            return None

        order_number = f"WO-{order_number_input.zfill(4)}"
        work_order = get_work_order(order_number)
        
        if work_order is None:
            return
        else:   # Unpack critical information
            (
            id,
            order_number,
            product_name,
            quantity,
            created_by,
            date_created,
            status
            ) = work_order
            return work_order
    
        
