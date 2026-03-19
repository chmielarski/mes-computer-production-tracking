from datetime import datetime
from menus.menu_utils import menu_header
from database.user_db import user_update
from database.user_statuses_db import get_user_status_map
from database.workstations_db import get_workstation_name_by_id
from database.workstation_sessions_db import create_workstation_session, end_workstation_session

# work station menu within while loop, inputs for work_order, station_name, and user
def menu_workstation(work_order, workstation_id, user_current):
    # user variable name definitions for menu header display
    username, role, user_number, employee_id = user_current
    statuses = get_user_status_map()
    workstation_name = get_workstation_name_by_id(workstation_id)

    # update user status to active and workstation to current workstation
    user_update(user_current, statuses["active"], workstation_name)  # Update user status to active and workstation to current workstation
    
    #create current workstation_session for user
    create_workstation_session(work_order, workstation_id, user_current)

    while True:
        # Display menu header 
        menu_header(f"{workstation_name.upper()}: {work_order[1]}", user_current)
        print("1. View Checklist")
        print("2. View BOM")
        print("3. Add Production Notes")
        print("4. Complete Checklist")
        print("5. Handoff to Next Station")
        print("0. Return to Work Order Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Viewing checklist...")
            # code to view checklist here

        elif choice == "2":
            print("Viewing BOM...")
            # code to view BOM here

        elif choice == "3":
            print("Adding production notes...")
            # code to add production notes here

        elif choice == "4":
            print("Completing checklist...")
            # code to complete checklist here

        elif choice == "5":
            print("Handing off to next station...")
            # code to hand off to next station here

        elif choice == "0":
            end_workstation_session(work_order, workstation_id, user_current)
            break  # Exit the workstation menu loop to return to previous menu

        else:
            print("Invalid choice. Please try again.")
