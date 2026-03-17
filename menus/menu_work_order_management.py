from database.work_order_db import create_work_order, edit_work_order, delete_work_order, view_all_work_orders
from database.user_db import user_update
from menus.menu_utils import menu_header

# work order management menu, with options to create WO, edit WO, delete WO, only available to users with role "admin"
def menu_work_order_management(user_current):
    
    while True:
        #update user table with user status and workstation
        user_update(user_current, "idle", None)  # Update user status to active and workstation to work order menu
        
        # remove previous text and display menu header function
        menu_header("WORK ORDER MANAGEMENT", user_current)
        
        #display options
        print("1. Create Work Order")
        print("2. Edit Work Order")
        print("3. Delete Work Order")
        print("4. View All Work Orders")
        print("0. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            
            menu_header("WORK ORDER LIST", user_current)
            create_work_order(user_current)
            #input("Press Enter to continue...") # user input requirement

        elif choice == "2":
            menu_header("WORK ORDER EDITOR", user_current)
            print("Enter the order number of the work order to edit:")
            order_number = input("Order Number: ")
            edit_work_order(order_number)
            #input("Press Enter to continue...") # user input requirement

        elif choice == "3":
            menu_header("WORK ORDER DELETION", user_current)
            print("Enter the order number of the work order to delete:")
            order_number = input("Order Number: ")
            delete_work_order(order_number)
            #input("Press Enter to continue...") # user input requirement

        elif choice == "4":
            menu_header("WORK ORDER LIST", user_current)
            work_orders = view_all_work_orders()
            print(f"{'ID':<5} | {'ORDER #':<10} | {'PRODUCT NAME':<20} | {'QUANTITY':<10} | {'CREATED BY':<15} | {'DATE CREATED':<20} | {'STATUS':<15}")
            for wo in work_orders:
                print(f"{wo[0]:<5} | {wo[1]:<10} | {wo[2]:<20} | {wo[3]:<10} | {wo[4]:<15} | {wo[5]:<20} | {wo[6]:<15}")
            input("Press Enter to continue...") # user input requirement

        elif choice == "0":
            break  # Exit the work order management menu loop to return to main menu

        else:
            print("Invalid choice. Please try again.")