import mysql.connector

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel_management"
    )

db = get_database_connection()
cursor = db.cursor()
