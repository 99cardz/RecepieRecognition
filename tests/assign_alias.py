import sqlite3
import random

database = "../schoenegge_rezepte.db"

conn = sqlite3.connect(database)
cursor = conn.cursor()

query = "SELECT count(*) FROM sqlite_master WHERE name = 'alias_table';"
cursor.execute(query)
if not cursor.fetchall()[0][0]:
    cursor.execute("CREATE TABLE alias_table (alias_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, alias_parent TEXT NOT NULL UNIQUE)")
    conn.commit()


query = "SELECT * FROM ingredients_table"
cursor.execute(query)
ingredients_content = cursor.fetchall()
query = "SELECT * FROM alias_table"
cursor.execute(query)
alias_content = cursor.fetchall()
alias_parent_list = [alias_content[1] for i in range(len(alias_content))]
#all_ingredients = [content[i][1] for i in range(len(content))]
#print(all_ingredients)
#print(content)

while ingredients_content:
    #print(">> %s ingredients left"%len(content))
    ingredient_tuple = ingredients_content[random.randint(0,len(ingredients_content)-1)]
    print(ingredient_tuple)
    if len(ingredient_tuple[1]) > 3:
        query = "SELECT * FROM ingredients_table WHERE ingredient LIKE ?"
        cursor.execute(query, ["%"+ingredient_tuple[1]+"%"])
        ingredient_like = cursor.fetchall()
        print("ingredients like %s"%ingredient_tuple[1], ingredient_like)
    hi = ingredient_tuple[1]
    input = input("parent-alias for - %s - >"%hi)
    query = "SELECT ingredient "


    ingredients_content.remove(ingredient_tuple)




conn.close()
