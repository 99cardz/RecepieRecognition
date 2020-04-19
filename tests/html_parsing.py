from bs4 import BeautifulSoup
import requests
import unicodedata
import random

def importUrls(file):
    list = []
    with open(file, "r") as file:
        raw_lines = file.readlines()
        for line in raw_lines:
            list.append(line.replace("\n", ""))
    return list

if __name__ == "__main__":
	url_list = importUrls("new_urls.txt")
	while url_list:
			url = url_list[random.randint(0, len(url_list)-1)]
			url = "https://schönegge.de/index.php/wir-bieten/rezepte/368-weisskohl"
			url_list.remove(url)
			print(url)
			raw_html = requests.get(url)
			#print(raw_html)
			soup = BeautifulSoup(raw_html.content, 'html.parser')
			#print(html)
			#print(type(html))
			item_page = soup.body.find("article", attrs={"class": "item-page"})
			new_soup = BeautifulSoup(item_page.prettify().replace("<br/>","\n"), "html.parser")

			print(new_soup.prettify())
			go = False
			for span in new_soup.select("span"):
				#print(span.text)
				if "Zubereitung" in span.text:
					go = False
				if go is True:
					print(span.text)
				if "Zutaten" in span.text:
					go = True

			"""page_list = list(item_page.prettify())
			del_flag = False

			for i in range(len(page_list)):
				#print(i)
				if page_list[i] is "<":
					del_flag = True
				#print(del_flag)
				if del_flag:
					print("deleting ", page_list[i])
					page_list[i] = ""
				if page_list[i] is ">":
					del_flag = False

			page_str = "".join(page_list)
			print(page_str)"""
