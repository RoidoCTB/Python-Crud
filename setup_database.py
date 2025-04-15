import sqlite3

# Connect to the database (creates it if it doesn't exist)
connection = sqlite3.connect("database.db")

# Open and read the SQL file
with open("tbl_student.sql", "r") as sql_file:
    sql_script = sql_file.read()

# Execute the SQL script
cursor = connection.cursor()
cursor.executescript(sql_script)

# Commit changes and close the connection
connection.commit()
connection.close()

print("Table created successfully from tbl_student.sql!")
