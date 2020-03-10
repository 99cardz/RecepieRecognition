import sqlite3
import sys

sorted_file = "sorted.txt"
recipe_file = "recipe.txt"
unit_file = "unit_list.txt"

data_database = "recipe_data.db"
recipe_database = "recipes.db"

class recipeLine:
    ingredient_list = []
    unit_str = ""
    amount_str = ""
    def description(self):
        desc_str = "%s %s %s" % (self.amount_str, self.unit_str, self.ingredient_list)
        return desc_str


def print_to_sorted_file(sorted_list):
    with open(sorted_file,"w") as file:
        file.seek(0)
        file.truncate()
        for line in sorted_list:
            file.write(str(line))
            file.write("\n")

def hasNumber(inputStr):
    return any(char.isdigit() for char in inputStr)

def readUnitFile():
    with open(unit_file) as file:
        unit_list = file.readlines()
        unit_list = [line[:-1]for line in unit_list]
        unit_list = [unit_list[n].lower()for n in range(0,len(unit_list))]
        print(*unit_list)
    return unit_list

def readUnitTable():
    try:
        sqliteConnection = sqlite3.connect(data_database)
        cursor = sqliteConnection.cursor()
        print("Connected to DB to retrieve Units")

        cursor.execute("""SELECT * from units_table""")
        records = cursor.fetchall()
        units = []
        for row in records:
            units.append(row[1])
    except sqlite3.Error as error:
        print("Error:", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("closed connection to DB")
        print("Units from DB: ", *units)
        return units

def addIngredientsToDb(recipe_class_object):
    ##retrieve all ingredients from recipe_class_object
    all_ingredients = []
    for line in recipe_class_object:
        for str in line.ingredient_list:
            all_ingredients.append(str)

    print(all_ingredients)

    print("### Inserting all missing Ingredients to Database ###")
    for ingredient in all_ingredients:
        try:
            sqliteConnection = sqlite3.connect(data_database)
            cursor = sqliteConnection.cursor()
            print("Connected to DB to add ingredient")
            insert_query = """INSERT INTO ingredient_table (ingredient)
                            VALUES (?);"""
            cursor.execute(insert_query, [ingredient],)
            sqliteConnection.commit()
            print("inserted ingredient * %s *" % (ingredient))

            cursor.close()

        except sqlite3.Error as error:
            print("error while inserting ingredient: ", error)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("closed connection to db")
    print("### Finished adding all non existing Ingredients to Database ###")
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

def interpretrecipe():
    ### IMPORT UNITS FROM DATABASE TABLE
    unit_list = readUnitTable()

    ###IMPORT recipe FROM recipe FILE
    recipe = importrecipe()

    recipe_line_list = [recipeLine() for i in range(len(recipe))]

    line_count = 0
    for line in recipe:
        print("********* line %s *********" % (line_count))
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
            print("no amount detected at line", line_count)
            for i in range(1, len(line)):
                ingredient_buffer.append(line[i])
        ##if first object is something else there is no ammount and ingredient is next object/objects
        else:
            print("no amount detected at line", line_count)
            print("no unit detected at line", line_count)
            ingredient_buffer = [line[i]for i in range(len(line))]
        #addIngredientToDb(rand_line.ingredient)#

        recipe_line_list[line_count].ingredient_list = interpretIngredient(ingredient_buffer)

        print("amount at line %s : %s" % (line_count, recipe_line_list[line_count].amount_str))
        print("unit at line %s : %s" % (line_count, recipe_line_list[line_count].unit_str))
        print("ingredient(s) at line %s : %s" % (line_count, recipe_line_list[line_count].ingredient_list))

        line_count+=1
    ##End For Loop of recipe lines
    return recipe_line_list
###End interpretrecipe()
if __name__ == '__main__':
    recipe = interpretrecipe()
    print(recipe[9].ingredient_list)

    addIngredientsToDb(recipe)
