
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

def hasNumber(inputStr):
    return any(char.isdigit() for char in inputStr)

def resetClass():
    rand_line.num = 0
    rand_line.amount = "no_amount"
    rand_line.unit = "no_unit"
    rand_line.ingriedient = "no_ingredient"
    rand_line.extra = "no_extra"

#unit_list = ["kg","g","l","liter","ml","stück","stk","kugel","kugeln","zehe","zehen","etwas","einige","packet","pck","pck.","m.-groãÿer"]
unit_file = open("unit_list.txt")
unit_list = unit_file.readlines()
unit_file.close()
unit_list = [line[:-1]for line in unit_list]
print(unit_list)

file = open("recepie.txt")
raw_lines = file.readlines()
file.close()
raw_lines = [line[:-1]for line in raw_lines]
raw_lines = [line.split()for line in raw_lines]
#raw_lines = [line.lower()for line in raw_lines]
print(raw_lines)

rand_line = RecepieLine()
num = 0
recepie_list = []
resetClass()
for line in raw_lines:
    rand_line.number = num

    if hasNumber(raw_lines[num][0]):
        rand_line.amount = raw_lines[num][0]
        rand_line.ingriedient = raw_lines[num][1]
    elif raw_lines[num][0].lower() in unit_list:
        rand_line.unit = raw_lines[num][0]
        print("no amount detected at line", num)
        rand_line.ingriedient = raw_lines[num][1]
    else:
        #rand_line.amount = "no_amount"
        print("no amount detected at line", num)
        rand_line.ingriedient = [raw_lines[num][i]for i in range(len(raw_lines[num]))]

    if len(raw_lines[num]) > 1 and raw_lines[num][1].lower() in unit_list:

        rand_line.unit = raw_lines[num][1]
        rand_line.ingriedient = raw_lines[num][2]
        print("yeah boi")

    #rand_line.unit = "kg"

    recepie_list.append(rand_line.description())

    resetClass()
    num+=1
print(recepie_list)
