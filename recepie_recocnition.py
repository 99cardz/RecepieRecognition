import sqlite3 as lite
import sys

sorted_file = "sorted.txt"
recepie_file = "recepie.txt"
unit_file = "unit_list.txt"

class RecepieLine:
    number = 0
    ingriedient = ""
    unit = ""
    amount = 0
    extra = ""
    def description(self):
        desc_str = "%s: %s %s %s %s" % (self.number, self.amount, self.unit, self.ingriedient, self.extra)
        #desc = self.number,": ", self.amount, self.unit, self.ingriedient
        return desc_str

def print_to_sorted_file(sorted_list):
    file = open(sorted_file,"w")
    file.seek(0)
    file.truncate()
    for line in sorted_list:
        file.write(str(line))
        file.write("\n")
    file.close()

def hasNumber(inputStr):
    return any(char.isdigit() for char in inputStr)

def resetClass():
    rand_line.num = 0
    rand_line.amount = "no_amount"
    rand_line.unit = "no_unit"
    rand_line.ingriedient = "no_ingredient"
    rand_line.extra = "no_extra"

<<<<<<< HEAD
=======

>>>>>>> parent of 34d5200... add desired public method
### IMPORT UNITS FROM UNIT FILE
with open("unit_list.txt") as unit_file:
    unit_list = unit_file.readlines()
    unit_list = [line[:-1]for line in unit_list]
    unit_list = [unit_list[n].lower()for n in range(0,len(unit_list))]
    print(*unit_list)

###IMPORT RECEPIE FROM RECEPIE FILE
with open(recepie_file) as file:
    recepie_list = file.readlines()
    recepie_list = [line[:-1]for line in recepie_list]
    recepie_list = [line.split()for line in recepie_list]
    print(*recepie_list)

rand_line = RecepieLine()
num = 0
recepie = []
resetClass()
for line in recepie_list:
    rand_line.number = num
    print("line %s" % (num))

    if hasNumber(recepie_list[num][0]):
        rand_line.amount = recepie_list[num][0]
        print("amount at line %s is %s" % (num, recepie_list[num][0]))
        rand_line.ingriedient = recepie_list[num][1]
        print("ingriedient at line %s is %s" % (num, recepie_list[num][1]))
    elif recepie_list[num][0].lower() in unit_list:
        rand_line.unit = recepie_list[num][0]
        print("unit at line %s is %s" % (num, recepie_list[num][0]))
        print("no amount detected at line", num)
        rand_line.ingriedient = recepie_list[num][1]
    else:
        #rand_line.amount = "no_amount"
        print("no amount detected at line", num)
        rand_line.ingriedient = [recepie_list[num][i]for i in range(len(recepie_list[num]))]

    if len(recepie_list[num]) > 1 and recepie_list[num][1].lower() in unit_list:

        rand_line.unit = recepie_list[num][1]
        print("unit at line %s is %s" % (num, recepie_list[num][1]))

        rand_line.ingriedient = recepie_list[num][2]
        print("ingriedient at line %s is %s" % (num, recepie_list[num][2]))


    #rand_line.unit = "kg"
    print(rand_line.description())
    recepie.append(rand_line.description())

    resetClass()
    num+=1
print(*recepie)
###EXPORT SORTED RECEPIE INTO SORTED FILE
print_to_sorted_file(recepie)
