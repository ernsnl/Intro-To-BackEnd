import mysql.connector
from mysql.connector import errorcode

TABLES = {}
TABLES['create_user'] = (
    "CREATE TABLE `User` ("
    "  `ID` int NOT NULL AUTO_INCREMENT,"
    "  `FirstName` varchar(25) NOT NULL,"
    "  `LastName` varchar(25) NOT NULL,"
    "  `UserName` varchar(50) NOT NULL,"
    "  `Email` varchar(250) NOT NULL,"
    "  `Password` varchar(64) NOT NULL,"
    "  `PasswordSalt` varchar(32) NOT NULL,"
    "   PRIMARY KEY (`ID`),"
    "   UNIQUE (`ID`)) ")

TABLES['create_blog'] = ("CREATE TABLE `BlogPost`("
                         "`ID` int NOT NULL AUTO_INCREMENT,"
                         "`BlogHtml` varchar(500) NOT NULL,"
                         "`CreatedDate` DATETIME NOT NULL,"
                         "`UpdatedDate` DATETIME NOT NULL,"
                         "`UserID` int,"
                         "UNIQUE (`ID`),"
                         "PRIMARY KEY (`ID`),"
                         "FOREIGN KEY (`UserID`) REFERENCES User(`ID`))")


def init_table(cnx):
    cursor = cnx.cursor()
    for name, ddl in TABLES.iteritems():
        try:
            print "Creating table {}: ".format(name)
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
