
import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "H@rd.Study123$"
)

c = mydb.cursor()