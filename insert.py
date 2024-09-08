from sqlite3 import Error

from connect import create_connection, database
from seed import create_task

def add_task_to_user(conn, task):
    """
    Create a new task for user
    :param conn:
    :param task:
    :return:
    """

    sql = '''
    INSERT INTO tasks(name,priority,status,project_id,begin_date,end_date) VALUES(?,?,?,?,?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, task)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid


if __name__ == '__main__':
    with create_connection(database) as conn:
# tasks
        task_1 = ('Analyze the requirements', "Analyze the requirements of the app", 1, 2)
        create_task(conn, task_1)

