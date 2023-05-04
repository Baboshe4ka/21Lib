import telebot
import json

from telebot import types
from api import *


class Book:
    def __init__(self, title):
        self.title = title
        self.author = None
        self.publish_date = None
        self.path = None

with open('src\config\conf.json', 'r') as bot_conf:
    conf = json.loads(bot_conf.read())

token = conf["bot_token"]  # значением вашего токена, полученного от BotFather
bot = telebot.TeleBot(token)

list_of_func = ['/add', '/list', '/find', '/take', '/delete'] #список реализованных функций 


#start 
@bot.message_handler(commands=['start'])  
def handle_start(message):

    if user_existence_check(message.from_user.id)== False:
        user_info = {
            'chat_id' : message.from_user.id,
            'first_name' : message.from_user.first_name,
            'last_name' : message.from_user.last_name,
            'user_name' : message.from_user.username
            }
        add_user(user_info)
    
    text = f"Привет, *{message.from_user.username}*.\nДобро пожаловать в чат бота-библиотеки!\nДля того чтобы выбрать нужную функциию используй команду */help*"
    bot.reply_to(message, text, parse_mode = 'Markdown')


@bot.message_handler(commands=['help'])
def handle_help(message):
    text = "Выберите нужное действие:"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width= 2, one_time_keyboard= True)
    markup.add(*list_of_func)

    bot.reply_to(message, text, reply_markup=markup)


#add
new_book_dict = {} 
@bot.message_handler(commands=['add'])
def handle_add(message):
    msg = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(msg, add_book_title)
    
def add_book_title(message):
    chat_id = message.chat.id
    title = message.text
    book = Book(title)
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
        if publish_date.lower() in  ['стоп', 'stop']:
            return
        msg = bot.reply_to(message, 'Некорректный ввод, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, add_book_publish_date)
        return
    
    book = new_book_dict[chat_id]
    book.publish_date = int(publish_date)
    book_info= vars(book)
    
    if book_existence_check(book_info) == False:
        msg = bot.send_message(chat_id, f"Отлично, кидай свою книгу!")
        bot.register_next_step_handler(msg, add_book_path)
    else:
        bot.send_message(chat_id, f"Такая книга уже существует")
        return
def add_book_path(message):
    chat_id = message.chat.id
    path = 'src/books/' + message.document.file_name
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open (path, 'wb') as new_book:
            new_book.write(downloaded_file)
        bot.reply_to(message, "Спасибо!")
    except Exception:
        bot.reply_to(message, "Что то пошло не так...\nВозможно файл слишком большой.")
    finally:   
        book = new_book_dict[chat_id]
        book.path = path   
        book_info= vars(book)
        add_book(book_info)
    
    new_book_dict.clear()
    

drop_book_dict = {}
@bot.message_handler(commands=['delete'])   
def drop_book(message):
    role = role_check(message.chat.id)
    if role == 'admin':
        msg= bot.reply_to(message, "Введите ID книги:")
        bot.register_next_step_handler(msg, drop_book_check)
    else:
        msg= bot.reply_to(message, "У вас нет прав для удаления книги.")

def drop_book_check(message):

    if not message.text.isdigit():
        if message.text.lower() in  ['стоп', 'stop']:
            return
        msg = bot.reply_to(message, 'Некорректный ввод, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, drop_book_check)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width= 2, one_time_keyboard= True)
    markup.add('Да', 'Нет')
    answ = message.text

    chat_id = message.chat.id

    book_info= book_id_serch(int(answ))
    book = Book(book_info[0][0])
    book.author = book_info[0][1]
    book.publish_date = book_info[0][2]
    drop_book_dict[chat_id] = book

    if len(book_info) != 0:
        msg= bot.send_message(chat_id, f"Найдена книга:{book_info[0][0]}/{book_info[0][1]}/{book_info[0][2]}.\nУдаляем?", reply_markup=markup)
        bot.register_next_step_handler(msg, drop_book)
    else: 
        bot.send_message(chat_id, "Книги с таким ID нет.")
    
def drop_book (message):
    chat_id = message.chat.id
    answer = message.text
    book = drop_book_dict[chat_id]
    if answer == 'Да':
        book_info= vars(book) 
        try:
            delete(book_info)
            bot.send_message(chat_id, "Книга удалена")
        except Exception:
            bot.send_message(chat_id, "Что-то пошло не так....")
    elif answer == 'Нет':
        bot.send_message(chat_id, "Не хочешь — как хочешь")
    drop_book_dict.clear()
    
    



#list
@bot.message_handler(commands=['list'])
def handle_list(message):
    list= list_of_books()
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Вот что у нас есть:")
    for book in list:
        bot.send_message(chat_id, f"ID: {book[0]}\nНазвание: {book[1]}\nАвтор: {book[2]}\nГод издания: {book[3]}")
    bot.send_message(chat_id, f"На этом всё.")
    



#find
find_book_dict = {} 
@bot.message_handler(commands=['find'])
def handle_find(message):
    msg = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(msg, find_book_title)

def find_book_title(message):
    chat_id = message.chat.id
    title = message.text
    book = Book(title)
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
    book = find_book_dict[chat_id]
    book.publish_date = int(publish_date)
    
    book_info= vars(book) 
    if book_existence_check(book_info):
        id = take_id(book_info)
        msg= bot.send_message(chat_id, f"Найдена книга: {book.title}/{book.author}/{book.publish_date}\nВот её ID: {id}")
    else:
        bot.send_message(chat_id, f"Такого у нас нет")
    
    find_book_dict.clear()
    

    

@bot.message_handler(commands=['take'])
def handle_take(message):
    msg = bot.reply_to(message, "Введите ID книги:")
    bot.register_next_step_handler(msg, take_book_id)

def take_book_id(message):
    chat_id = message.chat.id
    book_id = message.text
    book_path = take_book(book_id)
    bot.send_message(chat_id, f"Вот твоя книга:")
    bot.send_document(chat_id, document= open(book_path, 'rb'))


bot.infinity_polling()
