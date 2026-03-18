from database.db import get_connection

def get_workstation_map():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT workstation_id, workstation_name FROM workstations")
    rows = cursor.fetchall()

    conn.close()

    return {row[1]: row[0] for row in rows}

def get_workstation_name_by_id(workstation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT workstation_name FROM workstations WHERE workstation_id = ?", (workstation_id,))
    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None