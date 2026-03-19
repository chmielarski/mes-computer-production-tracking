from database.db import get_connection
from database.work_order_db import get_work_order_by_id, get_work_order_by_number
from datetime import datetime
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