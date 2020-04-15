import sqlite3

import os

database = "schoenegge_rezepte.db"

os.remove(database)

try:
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    cursor.execute("CREATE TABLE ingredients_table ( `ingredient_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `ingredient` TEXT NOT NULL UNIQUE)")
    cursor.execute("CREATE TABLE sources_table ( `recipe_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `source` TEXT NOT NULL UNIQUE )")
    #cursor.execute("CREATE TABLE sqlite_sequence(name,seq)")
    cursor.execute("CREATE TABLE units_table ( `unit_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `unit` TEXT NOT NULL UNIQUE )")
    sqliteConnection.commit()
except sqlite3.Error as error:
    print(error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
