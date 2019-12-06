import sqlite3
import sys

sorted_file = "sorted.txt"
recepie_file = "recepie.txt"
unit_file = "unit_list.txt"

database = "sorted_recepies.db"

class RecepieLine:
    ingredient_list = ""
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
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to DB to retrieve Units")

        cursor.execute("""SELECT * from Units""")
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

def addIngredientToDb(ingredient_list):

    #ingredients_to_add = [ingredients_to_add[n].replace(" ", "") for n in range(0, len(ingredients_to_add))]#jremove empty spaces
    ###add ingredient(s) to database
    print(ingredients_to_add)
    for i in range(len(ingredients_to_add)):
        try:
            sqliteConnection = sqlite3.connect(database)
            cursor = sqliteConnection.cursor()
            print("Connected to DB to add ingredient")
            insert_query = """INSERT INTO Ingredients (ingredient)
                            VALUES (?);"""
            insert_value = ingredients_to_add[i]
            cursor.execute(insert_query, [insert_value],)
            sqliteConnection.commit()
            print("inserted ingredient * %s *" % (insert_value))

            cursor.close()

        except sqlite3.Error as error:
            print("error while inserting ingredient: ", error)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("closed connection to db")
def identify_recepie_line():
    pass

def importRecepie():
    with open(recepie_file) as file:
        recepie_list = file.readlines()
        recepie_list = [line[:-1]for line in recepie_list]
        recepie_list = [line.split()for line in recepie_list]
        print(*recepie_list)
    return recepie_list

def interpretIngredient(ingredient_list):

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
        print("********* line %s *********" % (line_count))
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
            print("no amount detected at line", line_count)
            for i in range(1, len(line)):
                ingredient_buffer.append(line[i])
        ##if first object is something else there is no ammount and ingredient is next object/objects
        else:
            print("no amount detected at line", line_count)
            print("no unit detected at line", line_count)
            ingredient_buffer = [line[i]for i in range(len(line))]
        #addIngredientToDb(rand_line.ingredient)#

        recepie_line_list[line_count].ingredient_list = interpretIngredient(ingredient_buffer)

        print("amount at line %s : %s" % (line_count, recepie_line_list[line_count].amount_str))
        print("unit at line %s : %s" % (line_count, recepie_line_list[line_count].unit_str))
        print("ingredient(s) at line %s : %s" % (line_count, recepie_line_list[line_count].ingredient_list))

        line_count+=1
    ##End For Loop of recepie lines
    return recepie_line_list
###End interpretRecepie()
if __name__ == '__main__':
    recepie = interpretRecepie()
    ###EXPORT SORTED RECEPIE INTO SORTED FILE
    print(recepie[9].ingredient_list)
