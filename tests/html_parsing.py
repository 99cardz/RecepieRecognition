from bs4 import BeautifulSoup
import requests
import unicodedata

raw_html = requests.get("https://schönegge.de/index.php/wir-bieten/rezepte/112-vegetarische-thai-bolognese-mit-blumenkohl")
html = BeautifulSoup(raw_html.content, 'html.parser')
#print(type(html))

#print(html)

go = False

recipe = []
for p in html.select("span"):
	if p.text == "Zutaten":
#		print("start")
		go = True
	if p.text == "Zubereitung":
#		print("stop")
		go = False
	if go is True:
		print(unicodedata.normalize("NFKD",p.text))
		recipe.append(unicodedata.normalize("NFKD", p.text))
#	print(p.text)
#    if p['id'] == 'walrus':
#        print(p.text)

print(recipe)
print(*recipe)
for i in range(2):
	del(recipe[0])

for line in recipe:
	print(line)

print(recipe[1])


with open("test.txt", "w") as file:
	for line in recipe:
		file.write(line)
		file.write("\n")

