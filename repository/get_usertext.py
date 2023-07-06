import json
from config import site_url


def language_select(path1: str, path2: str):
    with open(path1, "r", encoding='utf-8') as read_file_menu:
        global data_lang_menu
        data_lang_menu = json.load(read_file_menu)
    with open(path2, "r", encoding='utf-8') as read_file_messages:
        global data_lang_messages
        data_lang_messages = json.load(read_file_messages)


language_select(r"languages/ru/ru.json", r"languages/ru/ru_messages.json")

commands_dict = {
    "🌐 Наш сайт": 
    ("markup = types.InlineKeyboardMarkup(row_width=1)", 
    f"button_site = (types.InlineKeyboardButton(data_lang_messages['main_menu']['redir_to_site'], url='{site_url}'))", 
    "markup.add(button_site)", "bot.send_message(message.chat.id, data_lang_messages['main_menu']['mes_redirect_to_site'], reply_markup=markup)"),
    "✅ Авторизация / Регистрация": 
    ("mes = bot.send_message(message.chat.id, data_lang_messages['auth']['auth_email'])", 
    "bot.register_next_step_handler(mes, check_email)"),
    "⚙️ Текущая мощность": ("bot.send_message(message.from_user.id, data_lang_messages['main_menu']['power_info'])",),
    "🔎 О нас": ("bot.send_message(message.from_user.id, data_lang_messages['main_menu']['about_as_info'])",),
    "Аккаунт": ("account(message)",),
    "Панель управления": ("control_panel(message)",),
    "Курсы криптовалют": ("rates_of_crypt(message)",),
    "Выход из аккаунта": ("rates_of_crypt(message)",),
    "Безопасность": ("secure(message)",),
    "Реферальная программа": ("referal_program(message)",),
    "Поддержка": ("support(message)",),
    "Изменить пароль": ("take_old_password(message)",)
}
