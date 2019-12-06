class Line:
	id = 0
	content = ""
	def desc(self):
		return self.id, self.content

recepie_raw = ["line1","line2"]

recepie_lines = [Line() for i in range(len(recepie_raw))]

recepie_lines[0].id = 12
recepie_lines[0].content = recepie_raw[0]

for i in range(len(recepie_lines)):
	print(recepie_lines[i].desc())

print(recepie_lines[0].desc())

