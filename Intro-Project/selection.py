from classes.user import User
import mysql.connector
from mysql.connector import errorcode


select_user_query = ('SELECT * FROM User')
select_user_by_id_query = "SELECT * FROM User WHERE ID = %(user_id)s"
select_user_by_email_query = "SELECT * FROM User WHERE Email Like %(email)s"
select_user_by_username_query = "SELECT * FROM User WHERE Username Like %(username)s"

def select_user(cnx, page=1, size=25):
    user_list = []
    cursor = cnx.cursor()
    try:
        cursor.execute(select_user_query)
        rows = cursor.fetchmany(page * size)
        for (id, first_name, last_name, username, email, password, passwordsalt) in rows:
            user_list.append(User(id, first_name, last_name,
                                  username, email, password, passwordsalt))
        print(user_list)
        return user_list
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("OK")


def select_user_by_email(cnx, email):
    cursor = cnx.cursor()
    try:
        cursor.execute(select_user_by_email_query, {'email': email})
        row = cursor.fetchone()
        if row is not None:
            _user = User._make(row)
            return _user
        else:
            return None
    except mysql.connector.Error as err:
        print(err.msg)

def select_user_by_username(cnx, username):
    cursor = cnx.cursor()
    try:
        cursor.execute(select_user_by_username_query, {'username': username})
        row = cursor.fetchone()
        if row is not None:
            _user = User._make(row)
            return _user
        else:
            return None
    except mysql.connector.Error as err:
        print(err.msg)

def select_user_by_id(cnx, user_id):
    cursor = cnx.cursor()
    cursor.execute(select_user_by_id_query,  {'user_id': user_id})
    row = cursor.fetchone()
    if row is not None:
        _user = User._make(row)
        return _user
    else:
        return None
