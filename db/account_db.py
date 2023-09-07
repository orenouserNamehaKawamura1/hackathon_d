import os, psycopg2, string, random, hashlib
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

def inset_ad_user(mail,pas):
    sql = 'INSERT INTO users VALUES (default, %s, %s, %s)' 
    salt = get_salt()
    hashed_password = get_hash(pas, salt)
    try :
        
        connection = DB.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,hashed_password,salt))
        count = cursor.rowcount 
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count

def login(mail,pas):
    sql = "SELECT pass, salt FROM users WHERE mail = %s AND delete_flag = 'f'"
    flg = False 
    try :
        connection = DB.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        mail = cursor.fetchone()
        if mail != None:
            salt = mail[1]
            
            hashed_password = get_hash(pas, salt)
            if hashed_password == mail[0]:
                flg = True
    except psycopg2.DatabaseError :
        flg = False
    finally : 
        cursor.close()
        connection.close()
    return flg

def select_userid(mail):
    connection = DB.get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id FROM users WHERE mail = %s'
    cursor.execute(sql,(mail,))
    id = cursor.fetchone()
    cursor.close()
    connection.close()
    return id

def ad_login(mail,pas):
    sql = "SELECT pass, salt FROM admin WHERE mail = %s"
    flg = False 
    try :
        connection = DB.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        mail = cursor.fetchone()
        if mail != None:
            salt = mail[1]
            
            hashed_password = get_hash(pas, salt)
            if hashed_password == mail[0]:
                flg = True
    except psycopg2.DatabaseError :
        flg = False
    finally : 
        cursor.close()
        connection.close()
    return flg




