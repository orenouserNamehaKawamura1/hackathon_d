import os, hashlib, psycopg2, string, random

class DB:
    
    def get_connection():
        url = os.environ['DATABASE_URL']
        connection = psycopg2.connect(url)
        return connection