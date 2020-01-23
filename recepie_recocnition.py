import sqlite3
import sys

sorted_file = "sorted.txt"
recepie_file = "recepie.txt"

data_database = "recepie_data.db"
recepie_database = "recepies.db"

class RecepieLine:
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

def addIngredientsToDb(recepie_class_object):
    ##retrieve all ingredients from recepie_class_object
    all_ingredients = []
    for line in recepie_class_object:
        for str in line.ingredient_list:
            all_ingredients.append(str)

    #print(all_ingredients)

    print("### Inserting all missing Ingredients to Database ###")
    for ingredient in all_ingredients:
        try:
            sqliteConnection = sqlite3.connect(data_database)
            cursor = sqliteConnection.cursor()
            print("Connected to DB to add ingredient")
            insert_query = """INSERT INTO ingredients_table (ingredient)
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

def importRecepie():
    with open(recepie_file) as file:
        recepie_list = file.readlines()
        recepie_list = [line[:-1]for line in recepie_list]
        recepie_list = [line.split()for line in recepie_list]
        print(*recepie_list)
    return recepie_list
###End inport Recepie()

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

def interpretRecepie():
    ### IMPORT UNITS FROM DATABASE TABLE
    unit_list = readUnitTable()

    ###IMPORT RECEPIE FROM RECEPIE FILE
    recepie = importRecepie()

    recepie_line_list = [RecepieLine() for i in range(len(recepie))]

    line_count = 0
    for line in recepie:
        ingredient_buffer = []
        ##if first object is a number its the amount
        if hasNumber(line[0]):
            recepie_line_list[line_count].amount_str = line[0]
            if line[1].lower() in unit_list:
                recepie_line_list[line_count].unit_str = line[1]
                for i in range(2, len(line)):
                    ingredient_buffer.append(line[i])
            else:
                for i in range(1, len(line)):
                    ingredient_buffer.append(line[i])
        ##if first object is in unit_list its the unit
        elif line[0].lower() in unit_list:
            recepie_line_list[line_count].unit_str = line[0]
            for i in range(1, len(line)):
                ingredient_buffer.append(line[i])
        ##if first object is something else there is no ammount and ingredient is next object/objects
        else:
            ingredient_buffer = [line[i]for i in range(len(line))]
        #addIngredientToDb(rand_line.ingredient)#

        recepie_line_list[line_count].ingredient_list = interpretIngredient(ingredient_buffer)
        line_count+=1
    ##End For Loop of recepie lines
    return recepie_line_list
###End interpretRecepie()

def addRecepieToDb(recepie):
    try:
        sqliteConnection = sqlite3.connect(recepie_database)
        cursor = sqliteConnection.cursor()
        print("Connected to recepie DB to add recepie")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #print(cursor.fetchall())
        id = len(cursor.fetchall())+1 ##Create new Table ID
        print("creating new table with id:", id)
        cursor.execute("""CREATE TABLE "%s" (
	               `amount`	TEXT,
	               `unit`	TEXT,
	               `ingredient`	TEXT);"""%id) ## creating new Table for recepies


    except sqlite3.Error as error:
        print("error while inserting recepie: ", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("closed connection to db")
###End addRecepieToDb()

"""def getIngredientID(ingredient_str):
    try:
        sqliteConnection = sqlite3.connect(data_database)
        cursor = sqliteConnection.cursor()
        print("Connected to recepie DB to retrieve ingredient ID of: %s" % (ingredient_str))
        """
if __name__ == '__main__':
    recepie = interpretRecepie()

    for line in recepie:
        print(line.description())
