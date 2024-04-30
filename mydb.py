import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'root',
)

cursorobject = dataBase.cursor()

cursorobject.execute("CREATE DATABASE elderco")

print("All Done!")