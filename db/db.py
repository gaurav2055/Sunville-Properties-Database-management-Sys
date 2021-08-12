import mysql.connector

con = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "sales"
)

cursor = con.cursor()



