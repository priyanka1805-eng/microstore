import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="microstore",
        user="postgres",
        password="Priya1805!",  # change this
        port="5432"
    )
