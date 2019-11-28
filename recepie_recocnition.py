import sqlite3
import sys

sorted_file = "sorted.txt"
recepie_file = "recepie.txt"
unit_file = "unit_list.txt"

database = "sorted_recepies.db"

class RecepieLine:
    number = 0
    ingredient = "no_ingredient"
    unit = "no_unit"
    amount = "no_amount"
    extra = "no_extra"
    def description(self):
        desc_str = "%s: %s %s %s %s" % (self.number, self.amount, self.unit, self.ingredient, self.extra)
        return desc_str

def write_to_db():
    sqliteConnection = sqlite.connect("Recepies.db")
    create_table = """CREATE TABLE Units (
                   id INTEGER PRIMARY KEY,
                   Unit TEXT NOT NULL);"""
    cursor = sqliteConnection.cursor()
    cursor.execute(create_table)
    sqliteConnection.commit()
    cursor.close()
    if (sqliteConnection):
        sqliteConnection.close()


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

def addToDb(ingredient_str):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to DB to add ingredient")
        #ingredient = "h"
        insert_query = """INSERT INTO Ingredients (ingredient)
                        VALUES (?);"""
        cursor.execute(insert_query, ingredient_str)
        sqliteConnection.commit()

        print("inserted ingredient")

        cursor.close()

    except sqlite3.Error as error:
        print("error while inserting ingredient: ", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("closed connection to db")

def main():
    ### IMPORT UNITS FROM DATABASE TABLE
    unit_list = readUnitTable()

    ###IMPORT RECEPIE FROM RECEPIE FILE
    with open(recepie_file) as file:
        recepie_list = file.readlines()
        recepie_list = [line[:-1]for line in recepie_list]
        recepie_list = [line.split()for line in recepie_list]
        print(*recepie_list)

    rand_line = RecepieLine()
    num = 0
    recepie = []
    for line in recepie_list:
        rand_line.number = num
        print("line %s" % (num))

        ##if first object is a number its the amount
        if hasNumber(recepie_list[num][0]):
            print("first object is a number")
            rand_line.amount = recepie_list[num][0]
            print("amount at line %s is %s" % (num, recepie_list[num][0]))
            if recepie_list[num][1].lower() in unit_list:
                rand_line.unit = recepie_list[num][1]
                print("unit at line %s is %s" % (num, recepie_list[num][1]))
                ingredient = []
                for i in range(2, len(line)):
                    ingredient.append(line[i])
                rand_line.ingredient = ingredient
            else:
                ingredient = []
                for i in range(1, len(line)):
                    ingredient.append(line[i])
                rand_line.ingredient = ingredient
                print("ingredient at line %s is %s" % (num, ingredient))
        ##if first object is in unit_list its the unit
        elif recepie_list[num][0].lower() in unit_list:
            print("first object is in unit_list")
            rand_line.unit = recepie_list[num][0]
            print("unit at line %s is %s" % (num, recepie_list[num][0]))
            print("no amount detected at line", num)
            ingredient = []
            for i in range(1, len(line)):
                ingredient.append(line[i])
            rand_line.ingredient = ingredient
        ##if first object is something else there is no ammount and ingredient is next object/objects
        else:
            print("first object is something else")
            print("no amount detected at line", num)
            print("no unit detected at line", num)
            print("ingredient at line %s is %s" % (num, [recepie_list[num][i]for i in range(len(recepie_list[num]))]))
            rand_line.ingredient = [recepie_list[num][i]for i in range(len(recepie_list[num]))]


        #rand_line.unit = "kg"
        #print(rand_line.ingredient)

        recepie.append(rand_line.description())
        addToDb(rand_line.ingredient)

        rand_line.num = 0
        rand_line.amount = "no_amount"
        rand_line.unit = "no_unit"
        rand_line.ingredient = "no_ingredient"
        rand_line.extra = "no_extra"

        num+=1
    return recepie
##End Main()
if __name__ == '__main__':
    for line in main():
        print(*line)

    ###EXPORT SORTED RECEPIE INTO SORTED FILE
