from database.db import get_connection

def get_work_order_map():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status_id, status_name FROM work_order_statuses")
    rows = cursor.fetchall()

    conn.close()

    return {row[1]: row[0] for row in rows}

def get_work_order_status_name_map():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status_id, status_name FROM work_order_statuses")
    rows = cursor.fetchall()

    conn.close()

    return {row[0]: row[1] for row in rows}