from bs4 import BeautifulSoup
import requests
import unicodedata

raw_html = requests.get("https://schönegge.de/index.php/wir-bieten/rezepte/112-vegetarische-thai-bolognese-mit-blumenkohl")
html = BeautifulSoup(raw_html.content, 'html.parser')
#print(type(html))

#print(html)

print(html.find(itemprop="articleBody").text.split())

for item in html.find(itemprop="articleBody"):
	print(type(item))
	print("hi")
