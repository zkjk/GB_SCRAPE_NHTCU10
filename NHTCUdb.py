import mysql.connector
from mysql.connector import Error
try:
    connection = mysql.connector.connect(host='127.0.0.1',
                             database='mydb',
                             user='mellumsu',
                             password='root')
    if connection.is_connected():
       InfoDB = connection.get_server_info()
       print("Connected to MySQL database... MySQL Server version on ",InfoDB)
       cursor = connection.cursor()
       cursor.execute("select database();")
       whichDB = cursor.fetchone()
       print ("Your connected to - ", whichDB)
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        
