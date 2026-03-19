from datetime import datetime
from menus.menu_utils import menu_header
from database.user_db import user_update
from database.user_statuses_db import get_user_status_map
from database.workstations_db import get_workstation_name_by_id
from database.workstation_sessions_db import create_workstation_session, end_workstation_session, get_workstation_sessions_is_handoff, handoff_workstation_session
from database.work_order_checklists_db import complete_work_order_checklist

# work station menu within while loop, inputs for work_order, station_name, and user
def menu_workstation(work_order, workstation_id, user_current):
    # user variable name definitions for menu header display
    username, role, user_number, employee_id = user_current
    statuses = get_user_status_map()
    workstation_name = get_workstation_name_by_id(workstation_id)

    
    # verify previous station is completed before allowing user to sign into current station, if not completed, display message that previous station must be completed before signing into current station, if completed, allow user to sign into current station and update user status to active and workstation to current workstation
    if workstation_id > 1:
        workstation_id_previous = workstation_id - 1
        workstation_is_handoff = get_workstation_sessions_is_handoff(work_order[0], workstation_id_previous)
        if workstation_is_handoff == 0:
            print("Previous station must be completed before signing into current station.")
            input("Press Enter to continue...")
            return

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
            # code to complete checklist here
            complete_work_order_checklist(work_order[0], workstation_id)
            print("Checklist completed.")
            input("Press Enter to continue...")

        elif choice == "5":
            # code to hand off to next station here
            handoff_workstation_session(work_order, workstation_id, user_current)
            print("Handoff to next station completed.")
            input("Press Enter to continue...")

        elif choice == "0":
            end_workstation_session(work_order, workstation_id, user_current)
            break  # Exit the workstation menu loop to return to previous menu