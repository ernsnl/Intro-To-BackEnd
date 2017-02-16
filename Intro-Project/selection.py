from classes.user import User
import mysql.connector
from mysql.connector import errorcode


select_user_query = ('SELECT * FROM User')
select_user_by_id_query = "SELECT * FROM User WHERE ID = %(user_id)s"


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
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


def select_user_by_id(cnx, user_id):
    cursor = cnx.cursor()
    cursor.execute(select_user_by_id_query,  {'user_id': user_id})
    row = cursor.fetchone()
    if row is not None:
        print 'creating user'
        _user = User._make(row)
        print _user.id
        return None
    else:
        return None
