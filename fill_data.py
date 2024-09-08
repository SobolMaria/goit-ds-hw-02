from faker import Faker
from connect import create_connection, database
from seed import create_user, create_status, create_task

fake = Faker()

def fill_users(conn, num_users=10):
    """ Додавання фейкових користувачів """
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        create_user(conn, (fullname, email))

def fill_statuses(conn):
    """ Додавання фіксованих статусів """
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        create_status(conn, (status,))

def fill_tasks(conn, num_tasks=20):
    """ Додавання фейкових завдань """
    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.paragraph(nb_sentences=3)
        status_id = fake.random_int(min=1, max=3)  
        user_id = fake.random_int(min=1, max=10)   
        create_task(conn, (title, description, status_id, user_id))

if __name__ == '__main__':
    with create_connection(database) as conn:
        if conn is not None:
            fill_users(conn, num_users=10)  
            fill_statuses(conn)            
            fill_tasks(conn, num_tasks=20) 
        else:
            print("Error! Cannot create the database connection.")