import requests


urls = []

with open("urls.txt","r") as file:
	lines = file.readlines()
	for line in lines:
		#print(line)
		if line not in urls:
			urls.append(line)

print("samples:")
for i in range(5):
    print(urls[i])

for i in range(len(urls)):

    print("copying : ",urls[i])
    raw_html = requests.get(urls[i])


    filename = "urls/%s.html"%i
    with open(filename, "w") as file:
        file.write(raw_html.text)

    with open("sources.txt", "a") as source_file:
        str = "%s %s"%(i, urls[i])
        print(str)
        source_file.write(str)
print("done!")
