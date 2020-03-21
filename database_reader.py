### programm to read the contents of recipe DATABA
import sqlite3

data_database = "recipe_data.db"
recipe_database = "recipes.db"


def readAllRecipes():
    try:
        sqliteConnection = sqlite3.connect(recipe_database)
        cursor = sqliteConnection.cursor()
        print("Connected to DB to retrieve recipes")

        cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name != 'sqlite_sequence';""")
        recipe_ammount = cursor.fetchone()[0]
        #print(recipe_ammount)
        for i in range(recipe_ammount):
            cursor.execute(""")
        #cursor.execute("""SELECT * from units_table""")
    except sqlite3.Error as error:
        print("Error:", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

if __name__ == '__main__':
    readAllRecipes()
