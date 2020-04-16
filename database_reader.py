### programm to read the contents of recipe DATABA
import sqlite3

recipe_database = "schoenegge_rezepte.db"

def RecipeAmount():
    try:
        sqliteConnection = sqlite3.connect(recipe_database)
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT count(recipe_id) FROM sources_table")
        recipe_amount = cursor.fetchone()[0]
    except sqlite3.Error as error:
        print("Error:", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            return recipe_amount

def RecipeNames():
    try:
        sqliteConnection = sqlite3.connect(recipe_database)
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT * FROM sources_table")
        list = cursor.fetchall()
    except sqlite3.Error as error:
        print("Error:", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            return list
def showRecipe(id):
    try:
        sqliteConnection = sqlite3.connect(recipe_database)
        cursor = sqliteConnection.cursor()

        query = "SELECT * FROM recipes_table WHERE recipe_id =?"
        cursor.execute(query, [id])
        recipe_raw = cursor.fetchall()
        #print(recipe_raw)
        for line in recipe_raw:
            amount = None
            unit = None
            ingredient = None

            amount = line[0]
            #print(type(line[1]))
            if line[1] is not None:
                query = "SELECT unit from units_table WHERE unit_id=?"
                cursor.execute(query, [line[1]])
                unit = cursor.fetchall()[0][0]
            if line[2] is not None:
                query = "SELECT ingredient from ingredients_table WHERE ingredient_id=?"
                cursor.execute(query, [line[2]])
                ingredient = cursor.fetchall()[0][0]
            print("%s - %s - %s" %(amount, unit, ingredient))
    except sqlite3.Error as error:
        print("Error:", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #return list
if __name__ == '__main__':
    recipe_list = RecipeNames()
    amount = len(recipe_list)
    print("there are %s Recipes" %amount)
    id_list = [str(recipe_list[i][0]) for i in range(amount)]
    #print(id_list)
    for recipe in recipe_list:
        print("id:%s > %s" %(recipe[0], recipe[1].replace("https://schönegge.de/index.php/wir-bieten/rezepte/", "")))
    while True:
        request = input("\nwhich recipe would you like to see? enter id! press any key to end!\n>>")
        if request in id_list:
            print("---showing recipe %s | %s---"%(request, recipe_list[int(request)][1].replace("https://schönegge.de/index.php/wir-bieten/rezepte/", "")))
            showRecipe(int(request))
        else:
            print("ending, bye!")
            break
