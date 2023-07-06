# import psycopg2
# from config import database
# from datetime import datetime
import json
# def wrapper(func):
#     def connect(*args, **kwargs):
#         try:
#             global cur
#             global con
#             con = psycopg2.connect(dbname=database["dbname"], user=database["user"], password=database["password"], host=database["host"])
#             cur = con.cursor()
#             func(*args, **kwargs)
#             con.commit()
#         # except psycopg2.Error:
#         #     if con:
#         #         con.rollback()
#         #         print('Request execution error!')
#         #         #ЗДЕСЬ НАДО КОЕ ЧТО СДЕЛАТЬ!!!!!!!!!!!!
#         #         #Исключения!!!!!
#         #         #КОГДА МЫ РЕГАЕМСЯ НЕ ОБРАБАТЫВАЕТСЯ ЧТО В БД УЖЕ ЕСТЬ ТАКОЙ ЕМАИЛ
#         finally:
#             if con:
#                 con.close()

#     return connect


# em_temp = 'test@mail.ru'
# now = str(datetime.now())
# now = now.split('.')


# connect = wrapper(lambda: cur.execute(f"UPDATE users SET activity = \'{now[0]}\' WHERE email = \'{em_temp}\'"))
# connect()
def language_select(path1: str, path2: str):
    with open(path1, "r", encoding='utf-8') as read_file_menu:
        global data_lang_menu
        data_lang_menu = json.load(read_file_menu)
    with open(path2, "r", encoding='utf-8') as read_file_messages:
        global data_lang_messages
        data_lang_messages = json.load(read_file_messages)

language_select(r"languages/ru/ru.json", r"languages/ru/ru_messages.json")
menus = [data_lang_menu[i][k]
    for i in data_lang_menu
    for k in data_lang_menu[i]
]

# for i in data_lang_menu:
#     for k in data_lang_menu[i]:
#         print(k)
print(menus)