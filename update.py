from sqlite3 import Error

from connect import create_connection, database

def update_status(conn, task_id, new_status_name):
    """
    Update the status of a specific task using the status name
    :param conn:
    :param task_id: ID of the task to update
    :param new_status_name: New status name 
    :return: None
    """
    sql = '''
    UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, (new_status_name, task_id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def update_name(conn, name_id, new_name):
    """
    Update the status of a specific task using the status name
    :param conn:
    :param task_id: ID of the task to update
    :param new_status_name: New status name 
    :return: None
    """
    sql = '''
    UPDATE users SET fullname = ? WHERE id = ?
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, (new_name, name_id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()   

if __name__ == '__main__':
    with create_connection(database) as conn:
        # Оновлення статусу завдання на 'in progress' для завдання з id=7
        update_status(conn, 7, 'in progress')
        update_name(conn, 1, 'Mariia Sobol')
