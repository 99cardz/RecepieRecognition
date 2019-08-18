
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

rand_line = RecepieLine()
num = 1

file = open("recepie.txt")
raw_lines = file.readlines()
raw_lines = [line[:-1]for line in raw_lines]
print(raw_lines)

recepie_list = []
for line in raw_lines:
    rand_line.number = num
    rand_line.ingriedient = "Mehl"
    rand_line.unit = "kg"
    rand_line.amount = "1.5"
    recepie_list.append(rand_line.description())
    num+=1
print(recepie_list)
