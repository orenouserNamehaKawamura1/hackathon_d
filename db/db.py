import os, hashlib, psycopg2, string, random

def get_connection():
    url = os.environ['_DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection