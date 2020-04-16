unique = []

with open("urls.txt","r") as file:
	lines = file.readlines()
	for line in lines:
		print(line)
		if line not in unique:
			unique.append(line)
			print("added line")


print(unique)


with open("urls.txt", "w") as file:
	for item in unique:
		file.write(item.replace("/index.php", "https://schönegge.de/index.php", 1))
