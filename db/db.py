import os
import hashlib
import psycopg2
import string
import random


class DB:

    def get_connection():
        url = os.environ['DATABASE_URL']
        connection = psycopg2.connect(url)
        return connection
