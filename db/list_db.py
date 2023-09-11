import os
import psycopg2


def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


# アカウント一覧
def ac_lists(page_num, per_page):
    sql = '''SELECT id, mail
         FROM users
         WHERE delete_flag = false
         ORDER BY id asc limit %s OFFSET %s'''

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (per_page, (page_num - 1) * per_page))
        users = cursor.fetchall()

    except psycopg2.DatabaseError:
        error = "エラーが発生しました。"

    finally:
        cursor.close()
        connection.close()

        return users


# usersテーブルのレコード数を取得
def ac_count():
    sql = "SELECT COUNT(*) FROM users WHERE delete_flag = false"

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, ())
        counts = cursor.fetchone()

    except psycopg2.DatabaseError:
        error = "エラーが発生しました。"

    finally:
        cursor.close()
        connection.close()

        return counts


# アカウント削除
def ac_delete(id):
    sql = "UPDATE users SET delete_flag = True WHERE id = %s"

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (id,))
        connection.commit()
        row = cursor.rowcount

    except psycopg2.DatabaseError:
        error = "エラーが発生しました。"

    finally:
        cursor.close()
        connection.close()

    return row


# 画像一覧
def img_list(page_num, per_page):
    sql = '''SELECT img_path
         FROM images
         WHERE delete_flag = false
         ORDER BY id asc limit %s OFFSET %s
        '''

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (per_page, (page_num - 1) * per_page))
        images = cursor.fetchall()

    except psycopg2.DatabaseError:
        error = "エラーが発生しました。"

    finally:
        cursor.close()
        connection.close()

        return images


# imagesテーブルのレコード数を取得
def img_count():
    sql = "SELECT COUNT(*) FROM images WHERE delete_flag = false"

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, ())
        counts = cursor.fetchone()

    except psycopg2.DatabaseError:
        error = "エラーが発生しました。"

    finally:
        cursor.close()
        connection.close()

        return counts
