import sqlite3
import sys
from bs4 import BeautifulSoup
import requests
import unicodedata
import random


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
"""
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
            insert_query = "INSERT INTO ingredient_table (ingredient)
                            VALUES (?);"
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
###End addIngredientsToDb"""

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
def retrieveIngredientID(ingredient_str, database):
    #print("retrieving ingredient ID for ingredient :" ,ingredient_str)
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        #print("Connected to %s to retrieve ID for : %s" % (data_database, ingredient_str))
        query = "SELECT ingredient_id FROM ingredients_table WHERE ingredient=?;"
        cursor.execute(query, [ingredient_str])
        output = cursor.fetchone()
        ingredient_ID = output[0]
    except sqlite3.Error as error:
        print("!!!error while retrieving INgredient ID\n", error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
                #print("closed connection to db")
        return ingredient_ID
###End retrieveIngredientID()
def retrieveUnitID(unit_str, database):
    #print("retrieving Unit id or adding unit: ", unit_str)
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        #print("Connected to %s to retrieve ID for : %s" % (data_database, ingredient_str))
        query = "SELECT unit_id FROM units_table WHERE unit=?;"
        cursor.execute(query, [unit_str])
        output = cursor.fetchall()
        #print(output, type(output))
        if len(output) is 0:
            #print("adding unit")
            query = "INSERT INTO units_table (unit) VALUES (?)"
            cursor.execute(query, [unit_str])
            sqliteConnection.commit()
            id = cursor.lastrowid
        else:
            id = output[0][0]
        #print("id is: ",id)
    except sqlite3.Error as error:
        print("!!!error while retrieving Unit ID\n", error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
                #print("closed connection to db")
        return id

def retrieveRecipeOnline(url_str):
    raw_html = requests.get(url_str)
    html = BeautifulSoup(raw_html.content, 'html.parser')

    go = False
    resume = False
    recipe = []

    for p in html.select("span"):
        if p.text == "Zutaten":
            go = True
            resume = True
        if p.text == "Zubereitung":
            go = False
            break
        if go is True:
            recipe.append(unicodedata.normalize("NFKD",p.text))
            #print(recipe[-1])

    if resume is False:
        return None

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

    recipe_id = getRecipeID(url, database)

    ignore_list = ["und","oder", "für", "die"]

    for line in recipe:
        print("> next line")

        known_units = getKnownUnits(database)
        known_ingredients = getKnownIngredients(database)

        amount = None
        unit = None
        ingredient = []

        if ":" in line:
            continue

        line_list = line.split()


        line_list = [line_list[n].lower().replace(",","") for n in range(0,len(line_list))]

        print("line content: %s"%(line_list))

        item_buffer = []
        while line_list:
            #print(line_list)
            if line_list[0] in ignore_list:
                del(line_list[0])
            elif hasNumber(line_list[0]):
                split_item = list(line_list[0])
                go_ahead = True
                for i in split_item:
                    if not i.isdigit():
                        go_ahead = False
                if go_ahead:
                    amount = line_list[0]
                    del(line_list[0])
                else:
                    print("!!item - %s - is not recocnisable du to there being a mixture of numbers and letters!!"%item)
                    amount = str(input("what is the amount? >"))
                    unit = str(input("what is the unit? >"))
                    del(line_list[0])
            elif line_list[0] in known_ingredients:
                item_buffer.append(line_list[0])
                del(line_list[0])
                ingredient.append(" ".join(item_buffer))
                #print(item_buffer, ingredient)
                item_buffer = []
            elif line_list[0] in known_units:
                unit = item
                del(line_list[0])
            elif longItem(line_list[0], line_list, database):
                line_list[0] = line_list[0] + " " + line_list[1]
                del(line_list[1])
                print("joined: ", line_list)
            else:
                print("item - %s - not known!" %line_list[0])
                input_str = input("i,u,o,a,j >>") #Ingredient, Unit, Other, Amount, Join
                if "j" in input_str:
                    item_buffer.append(line_list[0])
                    del(line_list[0])
                else:
                    item_buffer.append(line_list[0])
                    if input_str is "i":
                        ingredient.append(" ".join(item_buffer))
                        del(line_list[0])
                        item_buffer = []
                        #known_ingredients.append(ingredient)
                    elif input_str is "u":
                        unit = " ".join(item_buffer)
                        del(line_list[0])
                        item_buffer = []
                        #known_units.append(unit)
                    elif input_str is "o":
                        print("ignoring item - %s -"%line_list[0])
                        del(line_list[0])
                        #ignore_list.append(line_list[0])
                        #print("ignoring: ", ignore_list)
                        item_buffer = []
                    elif input is "a":
                        amount = str(input("what does the unknown translate to? >"))
                        del(line_list[0])
        ##end while
        if unit is not None:
            unit_id = retrieveUnitID(unit, database)
        else:
            unit_id = None
        if ingredient:
            for item in ingredient:
            #print(type(item))
                if item not in known_ingredients:
                    ingredient_id = addIngredientToDb(item, database)
                else:
                    #print(item)
                    ingredient_id = retrieveIngredientID(item, database)
                addLineToRecipeTable(amount, unit_id, ingredient_id, recipe_id, database)
                #print("added :", item)
            #print("added line to db")
def longItem(item, line, database):
    #print("checking")
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        query = "SELECT ingredient FROM ingredients_table WHERE ingredient LIKE ?;"
        cursor.execute(query, [item + "%"])
        output = cursor.fetchall()
        #print(output)
        #print(item, line)
        position = [i for i, x in enumerate(line) if x is item][0]
        #print(line[position] + " " + line[position+1])

        if output:
            for ingredient in output:
                #print(type(ingredient))
                #print(len(line), position)
                if line[position] + " " + line[position+1] == ingredient[0] and len(line) >= position+2:
                    #print("line+1")
                    return True
        else:
            return False
    except sqlite3.Error as error:
        print("error while searching for item\n", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def addIngredientToDb(ingredient, database):
    #print("adding new ingredient: ",ingredient)
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        query = "INSERT INTO ingredients_table(ingredient) VALUES (?);"
        #print(query)
        cursor.execute(query, [ingredient])
        sqliteConnection.commit()
        #print("added new ingredient %s to ingredients_table"%ingredient)
        id = cursor.lastrowid
    except sqlite3.Error as error:
        print("!!!!!!!!!error while adding ingredient to Table\n", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            return id
def addLineToRecipeTable(amount, unit_id, ingredient_id, recipe_id, database):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        query = "INSERT INTO R%s (amount, unit_id, ingredient_id) VALUES (?,?,?);"%recipe_id
        #print(query)
        cursor.execute(query, (amount, unit_id, ingredient_id))
        sqliteConnection.commit()
        #print("added new line to recipe %s"%recipe_id)
    except sqlite3.Error as error:
        print("!!!!!!!!!error while adding line to Table\n", error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
def addNewRecipeTable(url, database):
    #print(url, database)
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT count(source_id) FROM sources_table;")
        recipeID = cursor.fetchone()[0]
        #print(recipeID)
        cursor.execute(query)
        query = "INSERT INTO sources_table (recipe_id, source) VALUES (?, ?);"
        cursor.execute(query, (recipeID, url))
        sqliteConnection.commit()
        #print("inserted source")
    except sqlite3.Error as error:
        print("!!!!!!!!!error while adding id to source Table\n", error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
    return recipeID
def getKnownUnits(database):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        query = "SELECT * from units_table;"
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
        #print(units, type(units))
        return units
##ENd getKnownUnits()

def getKnownIngredients(database):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        query = "SELECT * from ingredients_table;"
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
        #print(ingredients, type(ingredients))
        return ingredients
def checkIfRecipeExists(url, database):
    flag = True
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        query = "SELECT recipe_id from sources_table WHERE source=?;"
        cursor.execute(query, [url])
        output = cursor.fetchall()
        #print(output)
        if output:
            flag = False
        #print(flag)
    except sqlite3.Error as error:
        print(error)
    finally:
        if (sqliteConnection):
                sqliteConnection.close()
        return flag

if __name__ == '__main__':

    recipe_database = "schoenegge_rezepte.db"
    url_list = importUrls("urls.txt")

    max = 5

    for i in range(max):

        #url = "https://schönegge.de/index.php/wir-bieten/rezepte/152-blumenkohl-brokkoli-gratin"
        url = url_list[random.randint(1, len(url_list))]

        print(">>> now processing ", url)

        if not checkIfRecipeExists(url, recipe_database):
            print("<<< recipe already exists in database!")
            i += 1
            continue

        raw_recipe = retrieveRecipeOnline(url)
        if raw_recipe is None:
            print("<<< Recipe unreadable, skipping...")
            i += 1
            continue

        recipe = processRecipe(raw_recipe, recipe_database, url)

        #addUrlToDb(recipe_database,url)

        #addRecipeToDb(recipe_database, recipe)
    #raw_recipe = retrieveRecipeOnline("https://schönegge.de/index.php/wir-bieten/rezepte/290-bananen-tiramisu")
    #print(raw_recipe)

    #recipe = interpretRecipe(raw_recipe)

    #print(recipe[0].amount_str)

    #addIngredientsToDb(recipe)

    #addRecipeToDb(recipe)
