import psycopg2


# This script is used to connect the user to the installed server with the password we setup as "password"
# This script also creates also creates the database in PostgreSQL for the project "Vandelay_db"
conn = psycopg2.connect(database='postgres', user='postgres',
                        password='password', host='localhost', port='5432')
conn.autocommit = True
cursor = conn.cursor()
create_db = 'CREATE database Vandelay_db'
cursor.execute(create_db)
print('New Database Created')
conn.close()
