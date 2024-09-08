import pandas as pd
from sqlite3 import Error

from connect import create_connection, database

def select_user_tasks(conn, user):
    '''Query all tasks of a specific user'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM tasks WHERE user_id=?', (user, ))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_tasks_by_status(conn, status):
    '''Query all tasks of with specific status'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?)', (status, ))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_users_without_task(conn):
    '''Query all users without task'''
    rows = None
    cur = conn.cursor()
    try:
        # Підзапит, який вибирає користувачів, що не мають завдань
        sql = '''
        SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)
        '''
        cur.execute(sql)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_not_completed_tasks(conn):
    '''Query all not finished tasks'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM tasks WHERE status_id NOT IN (3)')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_emails(conn, symbols):
    '''Query emails by specific symbols'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM users WHERE email LIKE ?', ('%' + symbols + '%',))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_by_status(conn):
    '''Query the number of tasks for each status'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(id) as total_tasks, status_id FROM tasks GROUP BY status_id')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_domenian_email(conn, domain):
    '''Query tasks assigned to users with a specific email domain'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT t.id, t.title, u.fullname, u.email FROM tasks AS t JOIN users AS u ON t.user_id = u.id WHERE u.email LIKE ?', ('%' + domain,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_blank_description(conn):
    '''Query a list of tasks that have no description'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT id, title FROM tasks WHERE description is NULL')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_users_with_status(conn):
    '''Query users and their tasks that are in ‘in progress’ status'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT u.fullname, t.title FROM users AS u INNER JOIN tasks AS t ON t.user_id = u.id WHERE t.status_id = (SELECT id FROM status WHERE name = "in progress")')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_users_tasks_qty(conn):
    '''Query users and the number of their tasks'''
    rows = None
    cur = conn.cursor()
    try:
        cur.execute('SELECT u.id, u.fullname, COUNT(t.id) AS task_count FROM users AS u LEFT JOIN tasks AS t ON t.user_id = u.id GROUP BY u.id, u.fullname')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

if __name__ == '__main__':
    with create_connection(database) as conn:

        tasks_by_user = select_user_tasks(conn, 7)
        print(pd.DataFrame(tasks_by_user, columns=['id', 'title', 'description', 'status_id', 'user_id']))

        tasks_by_status = select_tasks_by_status(conn, 'new')
        print(pd.DataFrame(tasks_by_status, columns=['id', 'title', 'description', 'status_id', 'user_id']))

        users_without_tasks = select_users_without_task(conn)
        for user in users_without_tasks:
            print(user)

        not_finished_tasks = select_not_completed_tasks(conn)
        print(pd.DataFrame(not_finished_tasks, columns=['id', 'title', 'description', 'status_id', 'user_id']))

        filter_emails = select_emails(conn, 'b')
        print(pd.DataFrame(filter_emails, columns=['id', 'fullname', 'email']))

        count_by_status = select_by_status(conn)
        print(count_by_status)

        find_tasks_with_domenian_email = select_domenian_email(conn, '@example.com')
        print(pd.DataFrame(find_tasks_with_domenian_email, columns=['id', 'title', 'fullname', 'email']))

        tasks_without_description = select_blank_description(conn)
        print(pd.DataFrame(tasks_without_description, columns=['id', 'title']))

        users_in_progress = select_users_with_status(conn)
        print(pd.DataFrame(users_in_progress, columns=['fullname', 'title']))

        qty_of_tasks = select_users_tasks_qty(conn)
        print(pd.DataFrame(qty_of_tasks, columns=['id', 'fullname', 'task_count']))
