from utils.utils import generate_random_string, hash_password
import mysql.connector
from mysql.connector import errorcode


insert_user_query = ("INSERT INTO User "
                     "(FirstName, LastName, UserName, Email, Password, PasswordSalt) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")


def insert_user(cnx, _user):
    cursor = cnx.cursor()
    salt = generate_random_string()
    print "aaaaaaaaaaaaaaaaaaaaa"
    print hash_password(_user.password, salt)
    data_user = (_user.first_name, _user.last_name, _user.username,
                     _user.email, hash_password(_user.password, salt), salt)
    try:
        cursor.execute(insert_user_query, data_user)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("OK")
