# **База данных и ее структура**

В качестве СУБД была выбрана SQLite. Выбор обоснован малым масштабом проекта и простотой работы с данной СУБД. Для корректной работы кода необходимо создать 2 таблицы (users, books), команда создания и структура которых описана ниже.

## Таблица users

Таблица users обладает следующей структурой:

```sql
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER UNIQUE,
	"first_name"	TEXT,
	"last_name"	TEXT,
	"user_name"	TEXT,
	"role"	TEXT DEFAULT 'user'
);
```

| id      | first_name | last_name | user_name | role |
| ------- | ---------- | --------- | --------- | ---- |
| INTEGER | TEXT       | TEXT      | TEXT      | TEXT |

- **id** - поле принимает telegram ID пользователля
- **first_name** - поле принимает имя пользователя (если оно указано в Telegram)
- **last_name** - поле принимает фамилию пользователя (если оно указано в Telegram)
- **user_name** - поле принимает Telegram username
- **role - поле** принимает роль пользователя. Используется для распределения доступа к функциям, значение по умолчанию user.

## Таблица books

Таблица books обладает следующей структурой:

```sql
CREATE TABLE IF NOT EXISTS "books" (
	"id"	INTEGER UNIQUE,
	"title"	TEXT,
	"author"	TEXT,
	"publish_date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
```

| id      | title | author | publish_date | path |
| ------- | ----- | ------ | ------------ | ---- |
| INTEGER | TEXT  | TEXT   | INTEGER      | TEXT |

- **id** - поле содержит ID книги, создаётся автоматически
- **title** - поле принимает название книги
- **author** - поле принимает имя автора
- **publish_date** - поле принимает год издания книги
- **path** - поле принимает путь до книги

# **api.py**

Файл [api.py](src\api.py) содержит в себе функции взаимодействия c базой данных. Основной библиотекой для взаимодействия является библиотека **sqlite3**.

Подключение к базе данных происходит с помощью json файла в папке [config](src\config). В файле должен быть путь до базы данных в папке [data](src\data) или в любой другой папке.

Для работы с базой данных используются следующие функции:

- **user_existence_check**
- **add_user**
- **role_check**
- **book_existence_check**
- **book_id_serch**
- **take_id**
- **add_book**
- **delete**
- **list_of_books**
- **take_book**

## user_existence_check

```python
def user_existence_check(user_id):
    res= cur.execute(f"SELECT * FROM users WHERE id = {user_id} ")
    if len(res.fetchall()) != 0:
        return True
    else:
        return False  
```

Функция принимает переменную ID пользователя и отправляет в базу данных запрос с поиском по указанному ID в таблице **users**.
В случае если пользоваетель уже записан в базе даннх то запрос в базу данных вернйт кортеж, длинна которого больше чем 0 и функция вернёт значение **True**. В противном случае функция возвращает **False**, обозначаем этим отсутсвие в базе данных пользователя с указанным ID.

## add_user

```python
def add_user(user_info):
    cur.execute(f"""INSERT INTO users (id, first_name, last_name, user_name)  
                VALUES ({user_info['chat_id']}, '{user_info['first_name']}', '{user_info['last_name']}', '{user_info['user_name']}'); """)
    con.commit()
```

Файл принимает информацию о пользователя от [telegram.py](src\telegram.py) и вносит информацию в соответсвующие поле в таблицу **user** в базе данных.

## role_check

```python
def role_check(user_id):
    res = cur.execute(f"SELECT role FROM users WHERE id = {user_id}""")
    role = res.fetchall() 
    return role[0][0]
```
Функция принимает переменную ID пользователя и отправляет в базу данных запрос с поиском по указанному ID. Результат запроса содержит кортеж с кортежем. Функция вовращает значение столбца *role* из таблицы **users**, обращаясь по индексу первого значаения первого элемента полученого от запроса результата. 

## book_existence_check

```python
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
```
Функция принимает словарь с информацией о книге и путём исполнения запроса проверяет наличие указаной книги в базе данных. В случае если книга уже записан в базе даннх то запрос в базу данных вернйт кортеж, длинна которого больше чем 0 и функция вернёт значение **True**. В противном случае функция возвращает **False**, обозначаем этим отсутсвие в базе данных искомой книги.

## book_id_serch

```python
def book_id_serch(book_id):
    res = cur.execute(f"SELECT title, author, publish_date FROM books WHERE id = {book_id}""")
    return res.fetchall()
```
Функция принимает ID книги, информацию о которой необходимо найти. Функцяи возвращяет название, автора и дату год публикации из таблицы **books** в виде кортежа с кортежем. 

## take_id

```python
def take_id(book):
    res = cur.execute(f"""SELECT id FROM books 
                    WHERE 
                        title = "{book['title']}" AND
                        author = "{book['author']}" AND
                        publish_date = "{book['publish_date']}"; """)
    id = res.fetchone()
    return id[0]
```
Функция принимает ID книги, которую нужно отправить. Функция возвращает значения столбца *path* из таблицы **books**, который представляет из себя путь до искомой книги. 

## add_book

```python
def add_book(book):
    if book_existence_check(book) == False:
        cur.execute(f"""INSERT INTO books (title, author, publish_date, path)
                    VALUES ("{book['title']}", "{book['author']}", {book['publish_date']}, "{book['path']}");""")
        con.commit()
        return True
    else:
        return False
```

Функция принимает словарь с информацией о книге, которую нужно добавить. Для того чтобы избежать повторения книга в базеданных функция образается к другой функции - *book_existence_check*. В случае если книга не был до этого занесена в таблице **books** то произойдёт ее записьи функция вернёт занчение **True**, в противном случает функция возвращает занчение **False**.  

## delete

```python
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
```
Функция принимает словарь с информацией о книге, которую нужно удалить. Для того чтобы удалить запись о книги так и саму книгу, первым делом выполняется запрос в базу данных для получения пути до удаляемой книги. После удаления функция исполняет запрос удаляющий запись с реквизитами книги из таблицы **books**.  


## list_of_books

```python
def list_of_books():
    res= cur.execute(f"SELECT id, title , author, publish_date FROM books")
    return res.fetchall()
```
Функция возвращяет кортеж с кортежами, содержащими информацию о всех книгах записаных в таблице **books**. 

## take_book

```python
def take_book(book_id):
    res= cur.execute(f"""SELECT path FROM books WHERE id = {book_id}""")
    book_path = res.fetchone()
    return book_path[0]
```
Функция принимает ID искомой книги и возвращает значение *path* из таблицы **books**, для того чтобы отправить пользователю нужную книгу. 

# **telegram.py**
