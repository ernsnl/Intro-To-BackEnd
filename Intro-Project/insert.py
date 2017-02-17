from utils.utils import generate_random_string, hash_password_sha256
import mysql.connector
from mysql.connector import errorcode


insert_user_query = ("INSERT INTO User "
                     "(FirstName, LastName, UserName, Email, Password, PasswordSalt) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")


def insert_user(cnx, _user):
    cursor = cnx.cursor()
    salt = generate_random_string()
    data_user = (_user.first_name, _user.last_name, _user.username,
                     _user.email, hash_password_sha256(_user.password, salt), salt)
    try:
        cursor.execute(insert_user_query, data_user)
        cnx.commit()
        _user.id = cursor.lastrowid
        _user.password = hash_password_sha256(_user.password, salt)
        _user.salt = salt
        print _user
        return _user
    except mysql.connector.Error as err:
        print(err.msg)
        return None
    else:
        print("OK")
