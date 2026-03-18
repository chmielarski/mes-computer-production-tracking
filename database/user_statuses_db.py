from database.db import get_connection

def get_user_status_map():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status_id, status_name FROM user_statuses")
    rows = cursor.fetchall()

    conn.close()

    return {row[1]: row[0] for row in rows}