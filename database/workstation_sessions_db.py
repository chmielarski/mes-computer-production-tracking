from datetime import datetime

from database.db import get_connection
from database.work_order_db import get_work_order_by_id, get_work_order_by_number


def create_work_order_report():
    work_order_number = input("Enter work order number for report: WO-")
    work_order = get_work_order_by_number("WO-" + work_order_number)
    if work_order is None:
        return
    
    conn = get_connection()
    cursor = conn.cursor()

    # get work order id from work order 
    work_order_id = work_order[0]

    # use work order id to get work order report data
    cursor.execute("""
        SELECT 
            wo.work_order_number,
            wo.product_name,
            wo.quantity,
            u.username,
            w.workstation_name,
            ws.start_time,
            ws.end_time,
            ws.labour_minutes
        FROM work_orders wo
        LEFT JOIN workstation_sessions ws 
            ON wo.work_order_id = ws.work_order_id
        LEFT JOIN users u 
            ON ws.user_number = u.user_number
        LEFT JOIN workstations w 
            ON ws.workstation_id = w.workstation_id
        WHERE wo.work_order_id = ?
    """, (work_order_id,))
    #using relational 

    work_order_report_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return work_order_report_data

# create a workstation_session with user_id and workstation_id
def create_workstation_session(work_order, workstation_id, user_current):
    conn = get_connection()
    cursor = conn.cursor()

    #work_order is tuple from work_orders table
    #user_current is tuple
    #session_id, work_order_id, user_number, workstation_id, start_time, end_time, labour_minutes, status
    
    work_order_id = work_order[0]
    user_number = user_current[2]
    start_time = datetime.now()
    end_time = None
    labour_minutes = None

    cursor.execute("""
        INSERT INTO workstation_sessions (work_order_id, workstation_id, user_number, start_time, end_time, labour_minutes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (work_order_id, workstation_id, user_number, start_time, end_time, labour_minutes))
    conn.commit()
    cursor.close()
    conn.close()

def end_workstation_session(work_order, workstation_id, user_current):
    conn = get_connection()
    cursor = conn.cursor()

    end_time = datetime.now()
    work_order_id = work_order[0]
    user_number = user_current[2]
    
    # Update the workstation session with end time and calculate labour minutes
    cursor.execute("""
        UPDATE workstation_sessions
        SET end_time = ?,
            labour_minutes = (julianday(?) - julianday(start_time)) * 24 * 60
        WHERE work_order_id = ? AND workstation_id = ? AND user_number = ? AND end_time IS NULL
    """, (end_time, end_time, work_order_id, workstation_id, user_number))
    conn.commit()
    cursor.close()
    conn.close()

# function to handle handoff between workstations, checks if previous workstation session for same work order has is_handoff status of 1, if not, prevents handoff and displays message that previous station must be completed before handoff can occur, if yes, allows handoff to occur and updates current workstation session with end time, labour minutes, and sets is_handoff to 1
def handoff_workstation_session(work_order, workstation_id, user_current):
    conn = get_connection()
    cursor = conn.cursor()

    work_order_id = work_order[0]
    user_number = user_current[2]
    end_time = datetime.now()

    # checklist must be complete before handoff
    cursor.execute("""
        SELECT is_completed
        FROM work_order_checklists
        WHERE work_order_id = ? AND workstation_id = ?
    """, (work_order_id, workstation_id))

    checklist = cursor.fetchone()

    if checklist is None or checklist[0] != 1:
        print("Checklist must be completed before handoff.")
        cursor.close()
        conn.close()
        return

    # update current active workstation session
    cursor.execute("""
        UPDATE workstation_sessions
        SET end_time = ?,
            labour_minutes = (julianday(?) - julianday(start_time)) * 24 * 60,
            is_handoff = 1
        WHERE work_order_id = ?
          AND workstation_id = ?
          AND user_number = ?
          AND end_time IS NULL
    """, (end_time, end_time, work_order_id, workstation_id, user_number))

    conn.commit()

    if cursor.rowcount == 0:
        print("No active session found to hand off.")
    else:
        print("Handoff completed successfully.")

    cursor.close()
    conn.close()

# function to get workstation_sessions for a work order, ordered by workstation sequence
def get_workstation_sequence(workstation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sequence_order
        FROM workstations
        WHERE workstation_id = ?
    """, (workstation_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return None

    return result[0]

# function to get workstation_sessions_is_handoff for a work order and workstation, to determine if handoff can occur to next station
def get_workstation_sessions_is_handoff(work_order_id, workstation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT is_handoff
        FROM workstation_sessions
        WHERE work_order_id = ? AND workstation_id = ? AND is_handoff = 1
    """, (work_order_id, workstation_id))
    
    is_handoff = cursor.fetchone()
    cursor.close()
    conn.close()
    return is_handoff[0] if is_handoff else 0

