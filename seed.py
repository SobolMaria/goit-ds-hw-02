from sqlite3 import Error

from connect import create_connection, database

def create_user(conn, user):
    """
    Create a new user into the projects table
    :param conn:
    :param user:
    :return: user id
    """
    sql = '''
    INSERT INTO users(fullname,email) VALUES(?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, user)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid

def create_status(conn, status):
    """
    Create a new task
    :param conn:
    :param status:
    :return:
    """

    sql = '''
    INSERT INTO status(name) VALUES(?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, status)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = '''
    INSERT INTO tasks(title,description,status_id,user_id) VALUES(?,?,?,?);
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
# create a new user
        user_1 = ('Mariia Sobol', 'mariia.sobol@email.com')
        user_id_1 = create_user(conn, user_1)

        user_2 = ('Anna Sobol', 'anna.sobol@email.com')
        user_id_2 = create_user(conn, user_2)

# create a new status
        status_id_1 = create_status(conn, ('new',))
        status_id_2 = create_status(conn, ('in progress',))
        status_id_3 = create_status(conn, ('completed',))

# create a new task
        task_1 = ('Task 1', 'Description for task 1', status_id_1, user_id_1)
        create_task(conn, task_1)
        task_2 = ('Task 2', 'Description for task 2', status_id_2, user_id_1)
        create_task(conn, task_2)
        task_3 = ('Task 3', 'Description for task 3', status_id_2, user_id_2)
        create_task(conn, task_3)

        

