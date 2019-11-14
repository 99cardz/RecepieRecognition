import sqlite3

def insertVaribleIntoTable(id, Unit):
    try:
        sqliteConnection = sqlite3.connect("Recepies.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO 'Units'
                          ("id", "Unit")
                          VALUES (?, ?);"""

        data_tuple = (id, Unit)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")
	sqlite_last_id =""" SELECT last_insert_rowid() """
	sqlite.execute(sqlite_last_id)
	sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

print("hi")
with open("unit_list.txt") as file:
	lines = file.readlines()
	print(lines)
	i = 1
	for line in lines:
		insertVaribleIntoTable(i, line)
		print(i, line)
		i+=1
		
