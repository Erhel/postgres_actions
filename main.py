import psycopg2
from config import config

def create_tables_with_data_transaction(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, first_name varchar(64) not null, last_name varchar(64) not null, email varchar(64))")
            cur.execute("""CREATE TABLE rooms (
                            id SERIAL PRIMARY KEY, 
                            number int not null, 
                            floor int not null, 
                            owner_id int not null, 
                            CONSTRAINT fk_users FOREIGN KEY(owner_id) REFERENCES users(id))""")

            cur.execute("""INSERT INTO users VALUES 
                            (default, 'Andrey', 'Volkov', 'andrey.volkov@yandex.ru'), 
                            (default, 'Maksim', 'Ivanov', 'maks_ivanov@gmail.com'), 
                            (default, 'Alexei', 'Medvedev', NULL)""")
            cur.execute("""INSERT INTO rooms VALUES 
                            (default, 103, 1, 1), 
                            (default, 104, 1, 1), 
                            (default, 211, 2, 3)""")
        conn.commit()
    except:
        conn.rollback()

def connect():
    conn = None
    try:
        params = config()
        
        conn = psycopg2.connect(**params)

        create_tables_with_data_transaction(conn)

        with conn:
            with conn.cursor() as cur:

                cur.execute("SELECT users.first_name, users.last_name, users.email, COUNT(*) as number_of_apartments FROM users JOIN rooms ON rooms.owner_id = users.id GROUP BY users.id")

                row = cur.fetchone()
                
                while row is not None:
                    print(row)
                    row = cur.fetchone()

                cur.execute("DELETE FROM users WHERE id = %s", "2")

                cur.close()

                conn.rollback()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()