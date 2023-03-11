from psycopg2 import connect
from pymongo import MongoClient

# PostgreSQL database configuration
PG_HOST = "localhost"
PG_PORT = 5432
PG_DATABASE = "userdetails_db"
PG_USERNAME = "postgres"
PG_PASSWORD = "12345"
pg_conn = connect(
    host=PG_HOST,
    port=PG_PORT,
    dbname=PG_DATABASE,
    user=PG_USERNAME,
    password=PG_PASSWORD,
)

# MongoDB database configuration
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE = "profile_db"
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client[MONGO_DATABASE]
