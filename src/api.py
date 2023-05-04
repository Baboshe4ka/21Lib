import sqlite3
import json

with open('src\config\conf.json', 'r') as bot_conf:
    conf = json.loads(bot_conf.read())

db_path = conf["db_path"]
con = sqlite3.connect(db_path,  check_same_thread=False)
cur = con.cursor()



def existence_check(book):
    res = cur.execute(f"""SELECT id FROM books 
                    WHERE 
                        title = "{book['title']}" AND
                        author = "{book['author']}" AND
                        publish_date = "{book['publish_date']}"; """)
    if len(res.fetchall()) == 0:
        return False
    else:
        return True
    
def take_id(book):
    res = cur.execute(f"""SELECT id FROM books 
                    WHERE 
                        title = "{book['title']}" AND
                        author = "{book['author']}" AND
                        publish_date = "{book['publish_date']}"; """)
    id = res.fetchone()
    return id[0]
     

def add(book):
    if existence_check(book) == False:
        cur.execute(f"""INSERT INTO books (title, author, publish_date)
                    VALUES ("{book['title']}", "{book['author']}", {book['publish_date']});""")
        con.commit()
        return True
    else:
        return False
    
def delete(book):
    if existence_check(book):
        cur.execute(f"""DELETE FROM books
                    WHERE
                        title = "{book['title']}" AND
                        author = "{book['author']}" AND
                        publish_date = "{book['publish_date']}";""")
        con.commit()
        return True
    else:
        return False
    
def list_of_books():
    res= cur.execute(f"SELECT id, title , author, publish_date FROM books")
    return res.fetchall()

def take_book(book_id):
    res= cur.execute(f"""SELECT path FROM books WHERE id = {book_id}""")
    book_path = res.fetchone()
    return book_path[0]


book_example = {'title' : "Postgres: Первое знакомство",
                'author': "Лузанов, Рогов, Лёвшин",
                'publish_date': "2023"}
def main():
    #print(existence_check(book_example))
    #print(add(book_example))
    #print(delete(book_example))
    #print(list_of_books())
    #print(take_id(book_example))
    print(take_book(1))
    pass
    


if __name__ == "__main__":
    main()
