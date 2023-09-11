import os
import psycopg2
import string
import random
import hashlib
from .db import DB


def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=30))
    return salt


def get_hash(pas, salt):
    b_pw = bytes(pas, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password


def inset_ad_user(mail, pas):
    sql = 'INSERT INTO users VALUES (default, %s, %s, %s)'
    salt = get_salt()
    hashed_password = get_hash(pas, salt)
    try:

        connection = DB.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail, hashed_password, salt))
        count = cursor.rowcount
        connection.commit()
    except Exception as e:
        print(e)
        count = 0
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count


def login(mail, pas):
    sql = "SELECT pass, salt FROM users WHERE mail = %s AND delete_flag = 'f'"
    flg = False
    try:
        connection = DB.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        mail = cursor.fetchone()
        if mail is not None:
            salt = mail[1]

            hashed_password = get_hash(pas, salt)
            if hashed_password == mail[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    return flg


def select_userid(mail):
    connection = DB.get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id FROM users WHERE mail = %s'
    cursor.execute(sql, (mail,))
    id = cursor.fetchone()
    cursor.close()
    connection.close()
    return id


def ad_login(mail, pas):
    sql = "SELECT pass, salt FROM admin WHERE mail = %s"
    flg = False
    try:
        connection = DB.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        mail = cursor.fetchone()
        if mail is not None:
            salt = mail[1]

            hashed_password = get_hash(pas, salt)
            if hashed_password == mail[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    return flg


def change_password(mail, pas):
    sql = '''
        UPDATE users
         SET pass = %s, salt = %s
         WHERE mail = %s AND delete_flag = 'f'
        '''
    salt = get_salt()
    new_hashed_password = get_hash(pas, salt)

    try:
        connection = DB.get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (new_hashed_password, salt, mail))
        connection.commit()
        count = cursor.rowcount

    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count


def change_ad_password(mail, pas):
    sql = 'UPDATE admin SET pass = %s, salt = %s WHERE mail = %s'
    salt = get_salt()
    new_hashed_password = get_hash(pas, salt)

    try:
        connection = DB.get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (new_hashed_password, salt, mail))
        connection.commit()
        count = cursor.rowcount

    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count
