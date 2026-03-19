from datetime import datetime

from database.workstation_sessions_db import create_work_order_report
from menus.menu_utils import menu_header    

def menu_work_order_report(user_current):
    
    while True:
        menu_header("WORK ORDER REPORT", user_current) # Display menu header
        print("1. Generate Work Order Report")
        print("0. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":

            menu_header("WORK ORDER REPORT", user_current)
            work_order_report_data = create_work_order_report()

            if work_order_report_data is not None:
                
                menu_header("WORK ORDER REPORT: " + work_order_report_data[0][0], user_current)
                total_labour = 0

                for row in work_order_report_data:

                    # format timestamps
                    start = datetime.fromisoformat(row[5]).strftime("%Y-%m-%d %H:%M:%S") if row[5] else "N/A"
                    end = datetime.fromisoformat(row[6]).strftime("%Y-%m-%d %H:%M:%S") if row[6] else "N/A"

                    # format labour minutes
                    labour = round(row[7], 2) if row[7] is not None else 0
                    total_labour += labour

                    print(f"Work Order: {row[0]}")
                    print(f"Product: {row[1]}")
                    print(f"Quantity: {row[2]}")
                    print(f"User: {row[3]}")
                    print(f"Workstation: {row[4]}")
                    print(f"Start: {start}")
                    print(f"End: {end}")
                    print(f"Labour Minutes: {labour}")
                    print("-" * 30)

                print(f"Total Labour Minutes: {round(total_labour, 2)}")
                input("Press Enter to continue...")

            

        elif choice == "0":
            break  # Exit the work order report menu loop to return to main menu

        