import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhara@123",
    database="hackereye"
)

cursor = conn.cursor()

sql = """
INSERT INTO users(username,email,password)
VALUES(%s,%s,%s)
"""

data = (
    "Supriya",
    "supriya@gmail.com",
    "1234"
)

cursor.execute(sql,data)

conn.commit()

print("User Added Successfully!")