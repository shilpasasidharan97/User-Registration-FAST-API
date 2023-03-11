from psycopg2 import connect

# Define the connection to the PostgreSQL database
PG_HOST = "localhost"
PG_PORT = 5432
PG_DATABASE = "user_db"
PG_USERNAME = "postgres"
PG_PASSWORD = "12345"
pg_conn = connect(
    host=PG_HOST,
    port=PG_PORT,
    dbname=PG_DATABASE,
    user=PG_USERNAME,
    password=PG_PASSWORD,
)
