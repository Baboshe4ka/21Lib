import telebot
import json

from telebot import types
from api import add, delete, existence_check


with open('src\config\conf.json', 'r') as bot_conf:
    conf = json.loads(bot_conf.read())

token = conf["bot_token"]  # значением вашего токена, полученного от BotFather
bot = telebot.TeleBot(token)

list_of_func = ['/add', '/delete'] #список реализованных функций 


#start 
@bot.message_handler(commands=['start'])  
def handle_start(message):
    text = f"Привет, *{message.from_user.username}*.\nДобро пожаловать в чат бота-библиотеки!\nДля того чтобы выбрать нужную функциию используй команду */help*"
    bot.reply_to(message, text, parse_mode = 'Markdown')

@bot.message_handler(commands=['help'])
def handle_help(message):
    text = "Выберите нужное действие:"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width= 2, one_time_keyboard= True)
    markup.add(*list_of_func)

    bot.reply_to(message, text, reply_markup=markup)



@bot.message_handler(commands=['echo'])
def handler_echo(message):
    name = message.from_user.first_name
    msg = bot.reply_to(message, f'{name}, тобой выбрана функция echo. Напиши мне что-нибудь и я напишу это в ответ.')
    bot.register_next_step_handler(msg, echo_reply)

def echo_reply(message):
    text = message.text
    chat_id  = message.chat.id
    bot.send_message(chat_id, f"Тобой было отправлено:\n{text}")




#add
new_book_dict = {} #Словарь для сбора информации о книге, которую нужно создать
class New_Book:
    def __init__(self, title):
        self.title = title
        self.author = None
        self.publish_date = None

@bot.message_handler(commands=['add'])
def handle_add(message):
    msg = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(msg, add_book_title)
    
def add_book_title(message):
    chat_id = message.chat.id
    title = message.text
    book = New_Book(title)
    new_book_dict[chat_id] = book
    
    msg= bot.send_message(chat_id, "Введите имя атора:")
    bot.register_next_step_handler(msg, add_book_author)

def add_book_author(message):
    chat_id = message.chat.id
    author= message.text
    book = new_book_dict[chat_id]
    book.author = author
    
    msg= bot.send_message(chat_id, "Введите год издания:")
    bot.register_next_step_handler(msg, add_book_publish_date)

def add_book_publish_date(message):
    chat_id = message.chat.id
    publish_date = message.text
    if not publish_date.isdigit():
        msg = bot.reply_to(message, 'Некорректный ввод, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, add_book_publish_date)
        return
    book = new_book_dict[chat_id]
    book.publish_date = int(publish_date)
    book_info= vars(book) #переменная содержит в себе словарь который передаётся в функцию для добавления в бдшку.
    
    if add(book_info):
        bot.send_message(chat_id, f"Отлично, Вы добавили книгу: {book.title}/{book.author}/{book.publish_date}")
    else:
        bot.send_message(chat_id, f"Такая книга уже существует")


#delete
drop_book_dict = {} #Словарь для сбора информации о книге, которую нужно создать
class Drop_Book:
    def __init__(self, title):
        self.title = title
        self.author = None
        self.publish_date = None

@bot.message_handler(commands=['delete'])   
def handle_delete(message):
    msg = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(msg, drop_book_title)
    
def drop_book_title(message):
    chat_id = message.chat.id
    title = message.text
    book = Drop_Book(title)
    drop_book_dict[chat_id] = book
    
    msg= bot.send_message(chat_id, "Введите имя атора:")
    bot.register_next_step_handler(msg, drop_book_author)

def drop_book_author(message):
    chat_id = message.chat.id
    author= message.text
    book = drop_book_dict[chat_id]
    book.author = author
    
    msg= bot.send_message(chat_id, "Введите год издания:")
    bot.register_next_step_handler(msg, drop_book_publish_date)

def drop_book_publish_date(message):
    chat_id = message.chat.id
    publish_date = message.text
    if not publish_date.isdigit():
        msg = bot.reply_to(message, 'Некорректный ввод, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, drop_book_publish_date)
        return
    book = drop_book_dict[chat_id]
    book.publish_date = int(publish_date)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width= 2, one_time_keyboard= True)
    markup.add('Да', 'Нет')
    book_info= vars(book) #Создаёт словарь с информацией для проверки существования книги
    if existence_check(book_info):
        msg= bot.send_message(chat_id, f"Найдена книга:{book.title}/{book.author}/{book.publish_date}.\nУдаляем?", reply_markup=markup)
        bot.register_next_step_handler(msg, drop_book)
    else: 
        bot.send_message(chat_id, "Такой книги нет.")
    
def drop_book (message):
    chat_id = message.chat.id
    answer = message.text
    book = drop_book_dict[chat_id]
    if answer == 'Да':
        book_info= vars(book) #Создаёт словарь с информацией о книге которую нужно удалить
        if delete(book_info):
            bot.send_message(chat_id, "Книга удалена")
        else:
            bot.send_message(chat_id, "Что-то пошло не так....")
    elif answer == 'Нет':
        bot.send_message(chat_id, "Не хочешь — как хочешь")
    



#list
@bot.message_handler(commands=['list'])
def handle_list(message):
    list= [
        {
        'title' : 'брух1',
        'author': 'лолкек',
        'publish_date': 1192
        }
     ] #переменная которая принимает список со словарями со всеми книгами из бдшки
    chat_id = message.chat.id
    for book in list:
        print(book)
        bot.send_message(chat_id, f"{book['title']}, {book['author']}, {book['publish_date']}")



#find
find_book_dict = {} #Словарь для сбора информации о книге, которую нужно найти
class Find_Book:
    def __init__(self, title):
        self.title = title
        self.author = None
        self.publish_date = None

@bot.message_handler(commands=['find'])
def handle_find(message):
    msg = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(msg, find_book_title)

def find_book_title(message):
    chat_id = message.chat.id
    title = message.text
    book = Find_Book(title)
    find_book_dict[chat_id] = book
    
    msg= bot.send_message(chat_id, "Введите имя атора:")
    bot.register_next_step_handler(msg, find_book_author)

def find_book_author(message):
    chat_id = message.chat.id
    author= message.text
    book = find_book_dict[chat_id]
    book.author = author
    
    msg= bot.send_message(chat_id, "Введите год издания:")
    bot.register_next_step_handler(msg, find_book_publish_date)

def find_book_publish_date(message):
    chat_id = message.chat.id
    publish_date = message.text
    if not publish_date.isdigit():
        msg = bot.reply_to(message, 'Некорректный ввод, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, find_book_publish_date)
        return
    book = drop_book_dict[chat_id]
    book.publish_date = int(publish_date)
    
    book_info= vars(book) #Создаёт словарь с информацией для проверки существования книги
    #здесь должна быть ветка событий зависящая от результата запроса в бдщку
    #msg= bot.send_message(chat_id, f"Найдена книга:{book.title}/{book.author}/{book.publish_date}")
    

#borrow
borrow_book_dict = {} #Словарь для сбора информации о книге, которую нужно найти
class Borrow_Book:
    def __init__(self, title):
        self.title = title
        self.author = None
        self.publish_date = None

@bot.message_handler(commands=['borrow'])
def handle_borrow(message):
    msg = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(msg, borrow_book_title)

def borrow_book_title(message):
    chat_id = message.chat.id
    title = message.text
    book = Borrow_Book(title)
    borrow_book_dict[chat_id] = book
    
    msg= bot.send_message(chat_id, "Введите имя атора:")
    bot.register_next_step_handler(msg, borrow_book_author)

def borrow_book_author(message):
    chat_id = message.chat.id
    author= message.text
    book = borrow_book_dict[chat_id]
    book.author = author
    
    msg= bot.send_message(chat_id, "Введите год издания:")
    bot.register_next_step_handler(msg, borrow_book_publish_date)

def borrow_book_publish_date(message):
    chat_id = message.chat.id
    publish_date = message.text
    if not publish_date.isdigit():
        msg = bot.reply_to(message, 'Некорректный ввод, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, borrow_book_publish_date)
        return
    book = drop_book_dict[chat_id]
    book.publish_date = int(publish_date)
    
    book_info= vars(book) #Создаёт словарь с информацией для проверки существования книги
    #здесь должна быть ветка событий зависящая от результата запроса в бдщку
    #msg= bot.send_message(chat_id, f"Найдена книга:{book.title}/{book.author}/{book.publish_date}")

#retrieve
@bot.message_handler(commands=['retrieve'])
def handle_retrieve(message):
    id = message.chat.id #создаёт айди пользователя для опраки его в бд 
    #Тут будет логика проверки взятых пользователем книг
    bot.send_message(chat_id, "Вы вернули книгу:")


#stats
stats_book_dict = {} #Словарь для сбора информации о книге, которую нужно найти
class Stats_Book:
    def __init__(self, title):
        self.title = title
        self.author = None
        self.publish_date = None
@bot.message_handler(commands=['stats'])
def handle_stats(message):
    msg = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(msg, stats_book_title)

def stats_book_title(message):
    chat_id = message.chat.id
    title = message.text
    book = Stats_Book(title)
    stats_book_dict[chat_id] = book
    
    msg= bot.send_message(chat_id, "Введите имя атора:")
    bot.register_next_step_handler(msg, stats_book_author)

def stats_book_author(message):
    chat_id = message.chat.id
    author= message.text
    book = borrow_book_dict[chat_id]
    book.author = author
    
    msg= bot.send_message(chat_id, "Введите год издания:")
    bot.register_next_step_handler(msg, stats_book_publish_date)

def stats_book_publish_date(message):
    chat_id = message.chat.id
    publish_date = message.text
    if not publish_date.isdigit():
        msg = bot.reply_to(message, 'Некорректный ввод, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, stats_book_publish_date)
        return
    book = drop_book_dict[chat_id]
    book.publish_date = int(publish_date)
    
    book_info= vars(book) #Создаёт словарь с информацией для проверки существования книги
    #здесь должна быть ветка событий зависящая от результата запроса в бдщку



bot.infinity_polling()
