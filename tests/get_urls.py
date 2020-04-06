from bs4 import BeautifulSoup
import requests

initial_html = requests.get("https://schönegge.de/index.php/wir-bieten/rezepte/72-apfel-bananen-muffins")

initial_content = BeautifulSoup(initial_html.content, 'html.parser')


with open("urls.txt", "w") as file:

	for a in initial_content.select("a"):
		print(a["href"])
		if "rezepte" in a["href"]:
			print("adding")
			file.write(a["href"])
			file.write("\n")

#<a class="mod-articles-category-title " href="/index.php/wir-bieten/rezepte/287-asia-salat-penne">Asia-Salat-Penne</a>

