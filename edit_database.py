import sqlite3

database = "schoenegge_rezepte.db"

def recipeAmount():
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    query = "SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name like 'R%' AND name not like '%table';"#type = 'table' AND name != 'sqlite_sequence' AND name !='units_table' AND name != 'ingredients_table' AND name != 'sources_table';"
    cursor.execute(query)
    output = cursor.fetchall()[0][0]
    sqliteConnection.close()
    print("found %s recipe tables"%output)
    if output:
        return output

#print(recipeAmount())
try:
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()

    query = "SELECT count(*) FROM sqlite_master WHERE name = 'recipes_table';"
    cursor.execute(query)
    if not cursor.fetchall()[0][0]:
        cursor.execute("CREATE TABLE recipes_table (amount TEXT, unit_id INTEGER, ingredient_id INTEGER, recipe_id INTEGER)")
        sqliteConnection.commit()

    amount = recipeAmount()
    if amount:
        for id in range(amount):
            print("processing recipe >%s"%id)
            query = "SELECT * FROM R%s"%id
            cursor.execute(query)
            output = cursor.fetchall()
            print("recipe content: " ,output)
            for line in output:
                new = line + (id,)
                query = "INSERT into recipes_table (amount, unit_id, ingredient_id, recipe_id) VALUES (?,?,?,?)"
                cursor.execute(query, new)
                sqliteConnection.commit()
            query = "DROP table R%s"%id
            cursor.execute(query)
            sqliteConnection.commit()
except sqlite3.Error as error:
    print(error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
