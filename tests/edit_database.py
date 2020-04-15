import sqlite3

database = "test_rezepte.db"

def recipeAmount(cursor):
    #sqliteConnection = sqlite3.connect(database)
    #cursor = sqliteConnection.cursor()
    query = "SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name != 'sqlite_sequence' AND name !='units_table' AND name != 'ingredients_table' AND name != 'sources_table';"
    cursor.execute(query)
    output = cursor.fetchone()[0]
    print(output)
    if output:
        return output

#print(recipeAmount())
try:
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    #cursor.execute("CREATE TABLE recipes_table (amount TEXT, unit_id INTEGER, ingredient_id INTEGER recipe_id INTEGER)")
    #sqliteConnection.commit()
    for i in range(recipeAmount(cursor)):
        pass
        #query = "SELECT * FROM R"
        #cursor.execute(query)
        #output = cursor.fetchall()
        #print(output)

except sqlite3.Error as error:
    print(error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
