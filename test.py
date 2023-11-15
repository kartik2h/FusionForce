import psycopg2

try:
    conn = psycopg2.connect(
        dbname='csvfile',
        user='postgres',
        password='1234',
        host='localhost',
        port='5433'
    )
    print("Database connected!")
except Exception as e:
    print("Could not connect to database.")
    print(e)
