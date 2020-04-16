import sqlite3

def importUrls(file):
    list = []
    with open(file, "r") as file:
        raw_lines = file.readlines()
        for line in raw_lines:
            list.append(line.replace("\n", ""))
    return list
##End importUrls()

database = "../schoenegge_rezepte.db"

conn = sqlite3.connect(database)
cursor = conn.cursor()
query = "SELECT source FROM sources_table"
cursor.execute(query)
output = cursor.fetchall()

existing = []
for tuple in output:
    existing.append(tuple[0])

all = importUrls("urls.txt")

with open("new_urls.txt", "w") as file:
    for url in all:
        if not url in existing:
            file.write(url + "\n")
