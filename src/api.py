import sqlite3
import json
import os

with open('src\config\conf.json', 'r') as bot_conf:
    conf = json.loads(bot_conf.read())

db_path = conf["db_path"]
con = sqlite3.connect(db_path,  check_same_thread=False)
cur = con.cursor()


def user_existence_check(user_id):
    res= cur.execute(f"SELECT * FROM users WHERE id = {user_id} ")
    if len(res.fetchall()) != 0:
        return True
    else:
        return False


def add_user(user_info):
    cur.execute(f"""INSERT INTO users (id, first_name, last_name, user_name)  
                VALUES ({user_info['chat_id']}, '{user_info['first_name']}', '{user_info['last_name']}', '{user_info['user_name']}'); """)
    con.commit()

def role_check(user_id):
    res = cur.execute(f"SELECT role FROM users WHERE id = {user_id}""")


def book_existence_check(book):
    res = cur.execute(f"""SELECT id FROM books 
                    WHERE 
                        title = "{book['title']}" AND
                        author = "{book['author']}" AND
                        publish_date = "{book['publish_date']}"; """)
    if len(res.fetchall()) == 0:
        return False
    else:
        return True

def book_id_serch(book_id):
    res = cur.execute(f"SELECT title, author, publish_date FROM books WHERE id = {book_id}""")
    return res.fetchall()


    
def take_id(book):
    res = cur.execute(f"""SELECT id FROM books 
                    WHERE 
                        title = "{book['title']}" AND
                        author = "{book['author']}" AND
                        publish_date = "{book['publish_date']}"; """)
    id = res.fetchone()
    return id[0]
     

def add_book(book):
    if book_existence_check(book) == False:
        cur.execute(f"""INSERT INTO books (title, author, publish_date, path)
                    VALUES ("{book['title']}", "{book['author']}", {book['publish_date']}, "{book['path']}");""")
        con.commit()
        return True
    else:
        return False
    
def delete(book):
    path_serch = cur.execute(f"""SELECT path FROM books
                WHERE
                    title = "{book['title']}" AND
                    author = "{book['author']}" AND
                    publish_date = "{book['publish_date']}";""")
    path = path_serch.fetchall()
    os.remove(path[0][0])
    cur.execute(f"""DELETE FROM books
                WHERE
                     title = "{book['title']}" AND
                     author = "{book['author']}" AND
                     publish_date = "{book['publish_date']}";""")
    con.commit()
    
def list_of_books():
    res= cur.execute(f"SELECT id, title , author, publish_date FROM books")
    return res.fetchall()

def take_book(book_id):
    res= cur.execute(f"""SELECT path FROM books WHERE id = {book_id}""")
    book_path = res.fetchone()
    return book_path[0]


book_example = {'title' : "Test",
                'author': "Test",
                'publish_date': "1234"}

user_example = {
            'chat_id' : 123456,
            'first_name' : 'Test',
            'last_name' : 'Test',
            'user_name' : 'Test'
            }
def main():
    #print(existence_check(book_example))
    #print(add(book_example))
    #delete(book_example)
    #print(list_of_books())
    #print(take_id(book_example))
    #print(take_book(1))
    #add_user(user_example)
    #print(book_id_serch(2))
    pass
    


if __name__ == "__main__":
    main()
