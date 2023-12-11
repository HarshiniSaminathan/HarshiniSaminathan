import psycopg2
from config import DATABASE_CONFIG

def dbconnection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

