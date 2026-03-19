from database.db import get_connection

# create work_order checklist
def create_work_order_checklist(work_order_id, job_type_id=1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT workstation_id FROM workstations ORDER BY sequence_order")
    workstations = cursor.fetchall()

    for ws in workstations:
        workstation_id = ws[0]

        cursor.execute("""
            INSERT INTO work_order_checklists 
            (job_type_id, work_order_id, workstation_id, is_completed)
            VALUES (?, ?, ?, 0)
        """, (job_type_id, work_order_id, workstation_id))

    conn.commit()
    conn.close()

def complete_work_order_checklist(work_order_id, workstation_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE work_order_checklists
            SET is_completed = 1
            WHERE work_order_id = ? AND workstation_id = ?
        """, (work_order_id, workstation_id))

        conn.commit()
        conn.close()    

def delete_work_order_checklist(work_order_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM work_order_checklists
        WHERE work_order_id = ?
    """, (work_order_id,))

    conn.commit()
    conn.close()