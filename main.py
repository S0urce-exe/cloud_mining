import telebot
import psycopg2
import json
from re import fullmatch, search, compile as compile_re
from telebot import types
from config import token, database
from repository.get_usertext import commands_dict
from datetime import datetime

data = []
marks = 0
is_authorized_ = False

bot = telebot.TeleBot(token)

def language_select(path1: str, path2: str):
    with open(path1, "r", encoding='utf-8') as read_file_menu:
        global data_lang_menu
        data_lang_menu = json.load(read_file_menu)
    with open(path2, "r", encoding='utf-8') as read_file_messages:
        global data_lang_messages
        data_lang_messages = json.load(read_file_messages)


def repository_select(path: str):
    pass


def language_selection_check(call):
    if ('data_lang_menu' in globals()) and ('data_lang_messages' in globals()):
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='English', callback_data='en'))
    markup.add(types.InlineKeyboardButton(text='Руский', callback_data='ru'))
    bot.send_message(message.chat.id, text="Select language. 🇬🇧\nВыберите язык. 🇷🇺", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def language_handler(call):
    if call.data == 'yes':
        reg_email(call.message)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, data_lang_messages["reg"]["cancel"])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


    if call.data == 'ru':
        language_select(r"languages/ru/ru.json", r"languages/ru/ru_messages.json")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        main_menu(call)
    elif call.data == 'en':
        language_select(r"languages/en/en.json", r"languages/en/en_messages.json")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        main_menu(call)


def is_menu(call):
    menus = [data_lang_menu[i][k]
    for i in data_lang_menu
    for k in data_lang_menu[i]
    ]
    return True if call.text in menus else False 


def reg_email(call):
    data.clear()
    ms = bot.send_message(call.chat.id, data_lang_messages["reg"]["em_for_reg"])
    bot.register_next_step_handler(ms, reg_psw)


def reg_psw(call):
    if not is_menu(call):
        if check_valid_email(call.text):
            data.append(call.text)
            ms = bot.send_message(call.chat.id, data_lang_messages["reg"]["pass_for_reg"])
            bot.register_next_step_handler(ms, final)
        else:
            bot.send_message(call.chat.id, data_lang_messages["auth"]["invalid_form_em"])
            mes = bot.send_message(call.chat.id, data_lang_messages["reg"]["em_for_reg"])
            bot.register_next_step_handler(mes, reg_email)
    else:
        bot.send_message(call.chat.id, data_lang_messages["reg"]["email_not_menu"])
        reg_email(call)


def final(call):
    def password_complexity_check(psw: str):
        res = [search(r"[a-z]", psw), search(r"[A-Z]", psw), search(r"[0-9]", psw), search(r"\W", psw)]
        if all(res):
            return True
        else:
            bot.send_message(call.chat.id, "🏗 " + data_lang_messages["unsafe_pass"]["mes_unsafe_pass"] +
                ("🔡" + data_lang_messages["unsafe_pass"]["lower_symb"])*(res[0] is None) +
                ("🔠" + data_lang_messages["unsafe_pass"]["upper_symb"])*(res[1] is None) +
                ("🔢" + data_lang_messages["unsafe_pass"]["numbes"])*(res[2] is None) +
                ("🔣" + data_lang_messages["unsafe_pass"]["special_symb"])*(res[3] is None))
            return False
    if password_complexity_check(call.text):
        global data
        def select_data():
            global temp_dct
            temp_dct = select_from_db(data[0])
        connect = wrapper(select_data)
        connect()
        if not temp_dct:
            data.append(call.text)
            connect = wrapper(lambda: cur.execute(f"INSERT INTO users (email, pass) VALUES (\'{data[0]}\', \'{data[1]}\')"))
            connect()
            del data
            bot.send_message(call.chat.id, data_lang_messages["reg"]["success_up"])
            buttons(call, data_lang_menu["main_menu"], "main_menu", data_lang_messages["main_menu"]["request"])
        else:
            bot.send_message(call.chat.id, data_lang_messages["reg"]["user_registered"])
            reg_email(call)
    else:
        ms = bot.send_message(call.chat.id, data_lang_messages["reg"]["pass_for_reg"])
        bot.register_next_step_handler(ms, final)


def main_menu(call):
    buttons(call.message, data_lang_menu["main_menu"], "main_menu", data_lang_messages["main_menu"]["request"])
    # bot.send_message(call.message.chat.id, data_lang["main_menu"]["request"])
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # website = types.KeyboardButton(data_lang["main_menu"]["site"])
    # sign = types.KeyboardButton(data_lang["main_menu"]["auth"])
    # equip_power = types.KeyboardButton(data_lang["main_menu"]["power"])
    # ab_as = types.KeyboardButton(data_lang["main_menu"]["about_as"])
    # markup.add(website, sign, equip_power, ab_as)
    # bot.send_message(call.message.chat.id, data_lang["main_menu"]["select_lang"], reply_markup=markup)


def wrapper(func):
    def connect(*args, **kwargs):
        try:
            global cur
            global con
            con = psycopg2.connect(dbname=database["dbname"], user=database["user"], password=database["password"], host=database["host"])
            cur = con.cursor()
            func(*args, **kwargs)
            con.commit()
        except psycopg2.Error:
            if con:
                con.rollback()
                print('Request execution error!')
                #Исключения!!!!!
        finally:
            if con:
                con.close()

    return connect


def control_panel(call):
    bot.send_message(call.chat.id, 'Панель управления скоро появится...')


# def support(message):
#     with open("support/needHelp.txt", "a", encoding="utf-8") as needHelpFile:
#         if message.chat.id > 0:
#             needHelpFile.write(str(message.chat.id) + "\n" + str(message.chat.first_name) + "\n")
#         else:
#             needHelpFile.write(str(message.chat.id) + "\n" + str(message.chat.title) + "\n")
#     with open("support/needHelp.txt", "a", encoding="utf-8") as supportFile:
#         supportTeam = set()
#         for line in supportTeam:
#             supportTeam.add(line.strip())
#     bot.send_message(message.chat.id, "Спасибо за вопрос, вам ответят в ближайшее время!")
#     for user in supportTeam:
#         if message.chat.id > 0:
#             bot.send_message(int(user), str(message.chat.id) + " (" + message.chat.first_name + "): " + message.text[message.text.find(' ')])
#         else:
#             bot.send_message(int(user), str(message.chat.id) + " (" + message.chat.title + "): " + message.text[message.text.find(' ')])


# def answer(message):
#     with open("support/support.txt", "r", encoding="utf-8") as supportFile:
#         supportTeam = set()
#         for line in supportFile:
#             supportTeam.add(line.strip())
#     if str(message.chat.id) in supportTeam:
#         needHelp = []
#         with open("support/needHelp.txt", "r", encoding="utf-8") as needHelpFile:
#             for line in needHelpFile:
#                 needHelp.append(line.strip())
#         for user in supportTeam:
#             if message.chat.id > 0:
#                 bot.send_message(user, str(message.chat.id) + " (" + message.chat.first_name + "): Answering to " + needHelp[0] + " (" + needHelp[1] + "): " + message.text[message.text.find(' ').format(message)]) 
#         bot.send_message(int(needHelp[0]), 'Support')
        

def rates_of_crypt(call):
    pass


def buttons(call, data: dict, menu: str, message: str):
    """
    The function is responsible for displaying the buttons.
    :param1: call or depending on the situation
    :param2: wireframe menu
    :param3: menu name
    :param4: message to display when menu is opened
    """
    data = tuple(data.keys())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #НЕ РАБОТАЕТ ШИРИНА МАРКАПА!!!!!!!!!!!
    buttons_data = []
    id = 0
    for i in range(len(data)):
        buttons_data.append(types.KeyboardButton(data_lang_menu[menu][data[id]]))
        id += 1
    for i in buttons_data:
        markup.add(i)
    bot.send_message(call.chat.id, message, reply_markup=markup)
    #Вынести в отдельные блоки в json сообщения


def client_menu(call):
    if is_authorized_:
        buttons(call, data_lang_menu["client_menu"], "client_menu", data_lang_messages["client_menu"]["message"])
    else:
        bot.send_message(call.chat.id, "Вы не авторизированы!")
    # bot.send_message(call.chat.id, data_lang["auth"]["success_in"])
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # cont_panel = types.KeyboardButton("Панель управления")
    # account = types.KeyboardButton("Аккаунт")
    # crypto_rates = types.KeyboardButton("Курсы криптовалют")
    # support = types.KeyboardButton("Поддержка")
    # back = types.KeyboardButton("Назад")
    # markup.add(cont_panel, account, crypto_rates, support, back)
    # bot.send_message(call.chat.id, data_lang["auth"]["use_menu"], reply_markup=markup)


def account(call):
    if is_authorized_:
        buttons(call, data_lang_menu["acc_settings"], "acc_settings", data_lang_messages["acc_settings"]["message"])
    else:
        bot.send_message(call.chat.id, "Вы не авторизированы!")
    # bot.send_message(call.chat.id, "Вы перешли в настройки аккаунта")
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # change_email = types.KeyboardButton("Изменить Email")
    # change_password = types.KeyboardButton("Изменить пароль")
    # two_auth = types.KeyboardButton("Двухфакторная ауентификация")
    # acc_activity = types.KeyboardButton("Активность аккаунта")
    # back = types.KeyboardButton("Назад")
    # markup.add(change_email, change_password, two_auth, acc_activity, back)
    # bot.send_message(call.chat.id, "Выберите необходимые настройки", reply_markup=markup)


def secure(call):
    if is_authorized_:
        buttons(call, data_lang_menu["secure"], "secure", data_lang_messages["secure"]["message"])
    else:
        bot.send_message(call.chat.id, "Вы не авторизированы!")


@bot.message_handler(content_types=['text'])
def menu_handler(message):
    #Нужен ли здесь дополнительный параметр (функция), который будет работать по принципу замыкания?.
    def enumeration_values(dict_key):
        """
        This function handles all menu items used by the user.
        WARNING! When given as a key to a tuple dictionary,
        consisting of 1 element, do not forget to put a comma at the end!
        :param1: the key whose corresponding value is performed by the function exec()
        """
        if message.text == dict_key:
            code_for_exec = commands_dict[message.text]
            for k in code_for_exec:
                    exec(k) 
    #Главное меню
    if language_selection_check(message):
        enumeration_values(data_lang_menu["main_menu"]["auth"])
        enumeration_values(data_lang_menu["main_menu"]["site"])
        enumeration_values(data_lang_menu["main_menu"]["power"])
        enumeration_values(data_lang_menu["main_menu"]["about_as"])
        #Клиент-меню
        enumeration_values(data_lang_menu["client_menu"]["account"])
        enumeration_values(data_lang_menu["client_menu"]["cont_panel"])
        enumeration_values(data_lang_menu["client_menu"]["crypto_rate"])
        enumeration_values(data_lang_menu["client_menu"]["logout"])
        #Настройки аккаунта
        enumeration_values(data_lang_menu["acc_settings"]["security"])
        enumeration_values(data_lang_menu["acc_settings"]["referal"])
        enumeration_values(data_lang_menu["acc_settings"]["support"])
        enumeration_values(data_lang_menu["secure"]["change_pass"])
    else:
        bot.send_message(message.chat.id, "Непорядок!!! Ты не выбрал язык!!!")

        
def check_valid_email(email: str):
    allowable = compile_re("([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if fullmatch(allowable, email):
        return True
    else:
        return False

#Изменение пароля - добавить подтверждение по email!!!

def take_old_password(call):
    mes = bot.send_message(call.chat.id, "Введите старый пароль")
    bot.register_next_step_handler(mes, take_new_password)


def take_new_password(call):
    old_pass = call.text
    def selection():
        cur.execute(f"SELECT * FROM users WHERE pass = \'{old_pass}\' AND email = \'{em_temp}\'")
        global out_data
        out_data = cur.fetchall()
    connect = wrapper(selection)
    connect()
    mes = bot.send_message(call.chat.id, "Введите новый пароль")
    bot.register_next_step_handler(mes, success_change_password)


def success_change_password(call):
    new_pass = call.text
    if out_data:
        connect = wrapper(lambda: cur.execute(f"UPDATE users SET pass = \'{new_pass}\' WHERE email = \'{em_temp}\'"))
        connect()
    else:
        bot.send_message(call.chat.id, "Ошибка ввода!")
    bot.send_message(call.chat.id, "Пароль успешно изменен!")

#Изменение email - пока шаблон!!!


def referal_program(call):
    bot.send_message(call.chat.id, 'Тут скоро будет реферальная программа...')
    

def select_from_db(email, password=None):
    """
    Эта функция должна быть в контексте connect()
    """
    if password is None:
        cur.execute(f"SELECT * FROM users WHERE email = \'{email}\'")
        #Тут заделать дыру, потенциальная опасность может быть в блоке else
    else:
        cur.execute(f"SELECT * FROM users WHERE pass = \'{password}\' AND email = \'{email}\'") #!!!!!!!!!!! ТУТ И НЕ ТОЛЬКО ТУТ ДОЛЖНО БЫТЬ КАК В POSTGRESQL введение с python!!!!!!!!!!!
    data = cur.fetchall()
    return data


def check_email(message):
    def replace_email(string: str):
        """
        This function replaces the entered email with asterisks
        """
        string = list(message.text)
        temp_1 = (0, 1, 2, -1, -2)
        temp_2 = ('@', '.', '_', '-')
        for id, symbol in enumerate(string):
            if (id in temp_1) or (symbol in temp_2):
                continue
            else:
                string.pop(id)
                string.insert(id, '*')
        return ''.join(string)
    global email_temp
    email_temp = message.text
    
    #ПРОВЕРКУ НА БАН ПОЛЬЗОВАТЕЛЯ ДОБАВЛЯТЬ СЮДА!!!

    em = replace_email(message.text)
    email_input = message.text
    def exec():
        data_from_db = select_from_db(email_input)
        if not is_menu(message):
            if check_valid_email(email_input):
                if data_from_db:
                    global em_temp
                    em_temp = data_from_db[0][1]
                    mes = bot.send_message(message.chat.id, data_lang_messages["auth"]["auth_pass"])
                    bot.register_next_step_handler(mes, check_password)
                    global marks
                    marks += 1
                elif not data_from_db:
                    #Вынести в отдельную функцию!!!
                    bot.send_message(message.chat.id, f'Введенный вами Email: {em} не зарегистрирован, желаете зарегистрироваться?')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    markup.add(types.InlineKeyboardButton(text=data_lang_messages["auth"]["yes"], callback_data='yes'))
                    markup.add(types.InlineKeyboardButton(text=data_lang_messages["auth"]["no"], callback_data='no'))
                    bot.send_message(message.chat.id, data_lang_messages["auth"]["yes_or_no"], reply_markup=markup)
            else:
                bot.send_message(message.chat.id, data_lang_messages["auth"]["invalid_form_em"])
                mes = bot.send_message(message.chat.id, data_lang_messages["auth"]["auth_email"])
                bot.register_next_step_handler(mes, check_email)
        else:
            bot.send_message(message.chat.id, data_lang_messages["reg"]["email_not_menu"])
            mes = bot.send_message(message.chat.id, data_lang_messages["auth"]["auth_email"])
            bot.register_next_step_handler(mes, check_email)
    connect = wrapper(exec)
    connect()


def check_password(message):
    psw_input = message.text
    def sign_psw():
        cur.execute(f"SELECT * FROM users WHERE pass = \'{psw_input}\' AND email = \'{em_temp}\'") #!!!!!!!!!!! ТУТ И НЕ ТОЛЬКО ТУТ ДОЛЖНО БЫТЬ КАК В POSTGRESQL введение с python!!!!!!!!!!!
        a = cur.fetchall()
        if a:
            global is_authorized_
            is_authorized_ = True
            client_menu(message)
            #Далее идёт простейшая реализация истории активности аккаунта
            now = str(datetime.now())
            now = now.split('.')
            cur.execute(f"UPDATE users SET activity = \'{now[0]}\' WHERE email = \'{em_temp}\'")
        elif not a:
            global marks
            marks += 1
            bot.send_message(message.chat.id, data_lang_messages["auth"]["wrong_pass"])
            mes = bot.send_message(message.chat.id, data_lang_messages["auth"]["auth_pass"])
            bot.register_next_step_handler(mes, check_password)
        else:
            bot.send_message(message.chat.id, data_lang_messages["auth"]["invalid_form_em"])
    global marks
    if marks < 5:
        connect = wrapper(sign_psw)
        connect()
    else:
        bot.send_message(message.chat.id, "Превышено максимальное число попыток входа с одного IP. Пожалуйста, попробуйте позже.")
        marks = 0
        connect = wrapper(lambda: cur.execute(f"UPDATE users SET is_blocked = true WHERE email = \'{em_temp}\'"))
        connect()
bot.polling(none_stop=True)
#!!!!!!!!!!!!!!!!!!ВЫНЕСТИ РЕГИСТРАЦИЮ И АВТОРИЗАЦИЮ В ОТДЕЛЬНЫЕ БЛОКИ!!!!!!!!!!!!!!!!!