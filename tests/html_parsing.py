from bs4 import BeautifulSoup
import requests

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
#		print(p.text)
		recipe.append(p.text)
#	print(p.text)
#    if p['id'] == 'walrus':
#        print(p.text)

for i in range(2):
	del(recipe[0])

for line in recipe:
	print(line)
