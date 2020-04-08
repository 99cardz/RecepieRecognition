import sqlite3
import sys
from bs4 import BeautifulSoup
import requests
import unicodedata


recipe_file = "recipe.txt"

data_database = "recipe_data.db"
recipe_database = "recipes.db"

class recipeLine:
    ingredient_list = []
    unit_str = ""
    amount_str = ""
    def description(self):
        desc_str = "%s %s %s" % (self.amount_str, self.unit_str, self.ingredient_list)
        return desc_str


def hasNumber(inputStr):
    return any(char.isdigit() for char in inputStr)

def readUnitTable():
    try:
        sqliteConnection = sqlite3.connect(data_database)
        cursor = sqliteConnection.cursor()
        #print("Connected to DB to retrieve Units")

        cursor.execute("""SELECT * from units_table""")
        records = cursor.fetchall()
        units = []
        for row in records:
            units.append(row[1])
    except sqlite3.Error as error:
        print(error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("closed connection to DB")
        print("Units from DB: ", *units)
        return units

def addIngredientsToDb(recipe_class_object):
    ##retrieve all ingredients from recipe_class_object
    all_ingredients = []
    for line in recipe_class_object:
        for str in line.ingredient_list:
            all_ingredients.append(str)

    #print(all_ingredients)

    #print("### Inserting all missing Ingredients to Database ###")
    for ingredient in all_ingredients:
        try:
            sqliteConnection = sqlite3.connect(data_database)
            cursor = sqliteConnection.cursor()
            #print("Connected to DB to add ingredient")
            insert_query = """INSERT INTO ingredient_table (ingredient)
                            VALUES (?);"""
            cursor.execute(insert_query, [ingredient])
            sqliteConnection.commit()
            #print("inserted ingredient * %s *" % (ingredient))

            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("closed connection to db")
    #print("### Finished adding all non existing Ingredients to Database ###")
###End addIngredientsToDb

def importrecipe():
    with open(recipe_file) as file:
        recipe_list = file.readlines()
        recipe_list = [line[:-1]for line in recipe_list]
        recipe_list = [line.split()for line in recipe_list]
        print(*recipe_list)
    return recipe_list
###End inport recipe()

def interpretIngredient(ingredient_list):
    #print("********")
    #print(ingredient_list)
    ###see if there are ingredients with multiple words
    ingredient_list = [ingredient_list[n].lower()for n in range(0,len(ingredient_list))]#lower every word in list

    ingredients_final = []
    ingredient_buffer = []
    canadd = False

    if len(ingredient_list) > 1:
        for i in range(len(ingredient_list)):
            if "," in ingredient_list[i]:
                ingredient_buffer.append(ingredient_list[i].replace(",",""))
                canadd = True
            else:
                ingredient_buffer.append(ingredient_list[i])
                canadd = False
            if canadd:
                if "" in ingredient_buffer:
                    ingredient_buffer.remove("")
                ingredients_final.append(" ".join(ingredient_buffer))
                ingredient_buffer = []
        ingredients_final.append(" ".join(ingredient_buffer))
    else:
        ingredients_final = ingredient_list

    return ingredients_final
###End interpretIngredient function

def interpretRecipe(recipe):
    ### IMPORT UNITS FROM DATABASE TABLE
    print(recipe)
    print("++**+++++++++++++")
    unit_list = readUnitTable()

    recipe = [line.split()for line in recipe]

    recipe_line_list = [recipeLine() for i in range(len(recipe))]

    line_count = 0
    for line in recipe:
        #print(line[0])
        #print(line)
        #print(type(line))
        #print("********* line %s *********" % (line_count))
        ingredient_buffer = []
        ##if first object is a number its the amount
        if hasNumber(line[0]):
            recipe_line_list[line_count].amount_str = line[0]
            if line[1].lower() in unit_list:
                recipe_line_list[line_count].unit_str = line[1]
                for i in range(2, len(line)):
                    ingredient_buffer.append(line[i])
            else:
                for i in range(1, len(line)):
                    ingredient_buffer.append(line[i])
        ##if first object is in unit_list its the unit
        elif line[0].lower() in unit_list:
            recipe_line_list[line_count].unit_str = line[0]

            #print("no amount detected at line", line_count)
            for i in range(1, len(line)):
                ingredient_buffer.append(line[i])
        ##if first object is something else there is no ammount and ingredient is next object/objects
        else:
            #print("no amount detected at line", line_count)
            #print("no unit detected at line", line_count)
            ingredient_buffer = [line[i]for i in range(len(line))]
        #addIngredientToDb(rand_line.ingredient)#

        #print(ingredient_buffer)
        recipe_line_list[line_count].ingredient_list = interpretIngredient(ingredient_buffer)

        #print("amount at line %s : %s" % (line_count, recipe_line_list[line_count].amount_str))
        #print("unit at line %s : %s" % (line_count, recipe_line_list[line_count].unit_str))
        #print("ingredient(s) at line %s : %s" % (line_count, recipe_line_list[line_count].ingredient_list))

        line_count+=1
    ##End For Loop of recipe lines
    #print("+++++++++++++++++++++++++++++++")
    return recipe_line_list
###End interpretRecipe()

def addRecipeToDb(recipe_class_object):
    print(recipe_class_object[0].unit_str)
    ##retrieve Ingredient ID:
    try:
        sqliteConnection = sqlite3.connect(recipe_database)
        cursor = sqliteConnection.cursor()
        cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name != 'sqlite_sequence';""")
        recipeID = cursor.fetchone()[0]
        #print(recipeID)
        cursor.execute("""CREATE TABLE Recipe%s(
            amount TEXT,
            unit INTEGER,
            ingredient INTEGER
        )"""%recipeID)
        for i in range(len(recipe_class_object)):
            for ingredient in recipe_class_object[i].ingredient_list:
                ingredientID = retrieveIngredientID(ingredient)
                insert_query = """INSERT INTO Recipe%s (amount, unit, ingredient) VALUES (?,?,?);"""%recipeID
                cursor.execute(insert_query, [recipe_class_object[i].amount_str, recipe_class_object[i].unit_str, ingredientID])
                sqliteConnection.commit()
                #print("inserted %s"%ingredient)
                #print(recipe_class_object[i].unit_str)
    except sqlite3.Error as error:
            print(error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
                #print("closed connection to db")


##End addRecipeToDb()
def retrieveIngredientID(ingredient_str):
    ingredient_ID = 0
    try:
        sqliteConnection = sqlite3.connect(data_database)
        cursor = sqliteConnection.cursor()
        #print("Connected to %s to retrieve ID for : %s" % (data_database, ingredient_str))
        query = """SELECT * from ingredient_table"""
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            #print(row)
            if row[1] == ingredient_str:
                ingredient_ID = row[0]
                #print("Ingredient ID of %s is %s" %(ingredient_str, row[0]))
                break
        if ingredient_ID == 0:
            print("############# Ingredient %s not found int Database #############" % (ingredient_str))

    except sqlite3.Error as error:
        print("error")
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
                #print("closed connection to db")
        return ingredient_ID
###End retrieveIngredientID()

def retrieveRecipeOnline(url_str):
    raw_html = requests.get(url_str)
    html = BeautifulSoup(raw_html.content, 'html.parser')

    go = False
    recipe = []

    for p in html.select("span"):
        if p.text == "Zutaten":
            go = True
        if p.text == "Zubereitung":
            go = False
            break
        if go is True:
            recipe.append(unicodedata.normalize("NFKD",p.text))
            #print(recipe[-1])

    for i in range(2):
        del(recipe[0])
    #print(recipe)
    #print(*recipe)

    return recipe
###End retrieveRecipeOnline()

def importUrls(file):
    list = []
    with open(file, "r") as file:
        raw_lines = file.readlines()
        for line in raw_lines:
            list.append(line.replace("\n", ""))
    return list
##End importUrls()

def processRecipe(recipe, database, url):

    recipe_id = addNewRecipeTable(url, database)

    known_units = getKnownUnits(database)
    known_ingredients = getKnownIngredients(database)
    recipe_dict = {}

    for line in recipe:
        print("> next line")

        amount = ""
        unit = ""
        ingredient = []

        line_list = line.split()
        line_list = [line_list[n].lower()for n in range(0,len(line_list))]

        item_buffer = []
        for item in line_list:
            if hasNumber(item):
                split_item = list(item)
                go_ahead = True
                for i in split_item:
                    if not i.isdigit():
                        go_ahead = False
                if go_ahead:
                    amount = item
            elif item in known_ingredients:
                ingredient.append(item)
            elif item in known_units:
                unit = item
            else:
                print("item %s not known!" %item)
                input_str = input("Choose i,u,o,a for ingredient, unit, other or ammount. If something is joined then add j.")
                if "j" in input_str:
                    item_buffer.append(item)
                else:
                    item_buffer.append(item)
                    if input_str is "i":
                        ingredient.append(" ".join(item_buffer))
                        item_buffer = []
                        known_ingredients.append(ingredient)
                    elif input_str is "u":
                        unit = " ".join(item_buffer)
                        item_buffer = []
                        known_units.append(unit)
                    elif input_str is "o":
                        print("nothing happens here yet!")
                    elif input is "a":
                        amount = str(input("what does the unknown translate to?"))
        #add amount, ingredient and unit of line to recipe table of database
        addLineToRecipeTable(amount, unit, ingredient, recipe_id, database)
        print("added line to db")
def addLineToRecipeTable(amount, unit, ingredient, recipe_id, database):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        query = """INSERT INTO R%s (amount, unit_id, ingredient_id) VALUES (?,?,?);"""%recipe_id
        cursor.execute(query, (amount, 1, 3))
    except sqlite3.Error as error:
        print("!!!!!!!!!error while adding Recipe Table\n", error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
def addNewRecipeTable(url, database):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name != 'sqlite_sequence' ;""")#AND name !='units_table' AND name != 'ingredient_table' AND name != 'source_table';""")
        recipeID = cursor.fetchone()[0]
        print(recipeID)
        cursor.execute("""CREATE TABLE R%s(
            amount TEXT,
            unit_id INTEGER,
            ingredient_id INTEGER;
        )"""%recipeID)
        query = """INSERT INTO sources_table (recipe_id, source) VALUES (?,?);"""
        cursor.execute(query, (recipeID, url))
    except sqlite3.Error as error:
        print("!!!!!!!!!error while adding Recipe Table\n", error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
    return recipeID
def getKnownUnits(database):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        query = """SELECT * from units_table;"""
        cursor.execute(query)
        records = cursor.fetchall()
        units = []
        for item in records:
            units.append(item[1])
    except sqlite3.Error as error:
        print(error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
        print(units, type(units))
        return units
##ENd getKnownUnits()

def getKnownIngredients(database):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        query = """SELECT * from ingredients_table;"""
        cursor.execute(query)
        records = cursor.fetchall()
        ingredients = []
        for item in records:
            ingredients.append(item[1])
    except sqlite3.Error as error:
        print(error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
        print(ingredients, type(ingredients))
        return ingredients

if __name__ == '__main__':

    recipe_database = "schoenegge_rezepte.db"
    url_list = importUrls("urls.txt")

    for url in url_list:

        ### >> need check for url/recipe already existing!!!!!

        print(">>> now processing ", url)
        raw_recipe = retrieveRecipeOnline(url)
        recipe = processRecipe(raw_recipe, recipe_database, url)

        #addUrlToDb(recipe_database,url)

        #addRecipeToDb(recipe_database, recipe)
    #raw_recipe = retrieveRecipeOnline("https://schönegge.de/index.php/wir-bieten/rezepte/290-bananen-tiramisu")
    #print(raw_recipe)

    #recipe = interpretRecipe(raw_recipe)

    #print(recipe[0].amount_str)

    #addIngredientsToDb(recipe)

    #addRecipeToDb(recipe)
