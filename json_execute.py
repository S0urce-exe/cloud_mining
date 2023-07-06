import json


def write_to_json(dict_file, path):
    with open(path, "w") as write_file:
        json.dump(dict_file, write_file)


#МОЖЕТ БЫТЬ ВЫНЕСТИ ВСЕ СООБЩЕНИЯ ОТДЕЛЬНО?


data = {
    "main_menu": {
        "site": "🌐 Наш сайт",
        "auth": "✅ Авторизация / Регистрация",
        "power": "⚙️ Текущая мощность",
        "about_as": "🔎 О нас"
    },
    "client_menu": {
        "account": "Аккаунт",
        "cont_panel": "Панель управления",
        "crypto_rate": "Курсы криптовалют",
        "logout": "Выход из аккаунта"
    },
    "acc_settings": {
        "security": "Безопасность",
        "referal": "Реферальная программа",
        "support": "Поддержка",
        "back": "Назад",
    },
    "secure": {
        "change_pass": "Изменить пароль",
        "change_email": "Изменить Email",
        "acc_activity": "Активность аккаунта",
        "back": "Назад",
    }
}

messages = {
    "main_menu": {
        "select_lang": "Вы выбрали русский язык!",
        "request": "Пожалуйста, выберите раздел.",
        "mes_redirect_to_site": "Нажмите на кнопку, для перехода на сайт.",
        "power_info": "Информация о текущей мощности.",
        "redir_to_site": "Переход на сайт.",
        "about_as_info": "Информация о нас."
    },
    "auth": {
        "auth_email": "Введите Email для авторизации.",
        "invalid_form_em": "Невеный формат Email.",
        "auth_pass": "Введите пароль для авторизации.",
        "em_not_found": "Введенный Вами Email: не зарегистрирован, желаете зарегистрироваться?",
        "wrong_pass": "Неверный пароль.",
        "yes_or_no": "Нажмите на кнопку ДА/НЕТ",
        "success_in": "Вы успешно вошли в аккаунт!",
        "use_menu": "Воспользуйтесь пунктами меню для навигации.",
        "yes": "Да",
        "no": "Нет"
    },
    "reg": {
        "user_registered": "Данный пользователь уже зарегистрирован!",
        "em_for_reg": "Введите Email для регистрации.",
        "pass_for_reg": "Введите пароль для регистрации",
        "email_not_menu": "Вы выбрали пункт меню, а нужно ввести Email",
        "success_up": "Вы успешно зарегистрировались!\n\nТеперь Вы можете авторизироваться!",
        "cancel": "Отмена регистрации"
    },
    "unsafe_pass": {
        "mes_unsafe_pass": "Введенный пароль ненадежен.\n\nРекомендуем добавить:\n\n",
        "lower_symb": "Символы нижнего регистра.\n\n",
        "upper_symb": "Символы верхнего регистра.\n\n",
        "numbes": "Цифры.\n\n",
        "special_symb": "Специальные символы."
    },
    "client_menu": {
        "message": "Вы находитесь в разделе управления"
    },
    "acc_settings": {
        "message": "Вы в настройках аккаунта"
    },
    "secure": {
        "message": "Вы в настройках безопасности аккаунта"
        #ТУТ КОЕ ЧТО ПОДДЕЛАТЬ!!!
    }
}

#Раскоментировать тот фрагмент, что ниже для английской локализации


# data = {
#     "main_menu": {
#         "site": "🌐 Our site",
#         "auth": "✅ Authorization / Registration",
#         "power": "⚙️ Current power",
#         "about_as": "🔎 About us",
#         "select_lang": "You have selected English!",
#         "request": "Please select a section.",
#         "mes_redirect_to_site": "Click the button to go to the site.",
#         "power_info": "Information about the current power.",
#         "redir_to_site": "Going to the site.",
#         "about_as_info": "Information about us."
#     },
#     "auth": {
#         "auth_email": "Enter your email to authenticate.",
#         "invalid_form_em": "Invalid email format.",
#         "auth_pass": "Enter password for authorization.",
#         "em_not_found": "The email you entered is not registered, would you like to register?",
#         "wrong_pass": "Wrong password.",
#         "yes_or_no": "Press the YES/NO button.",
#         "success_in": "You have successfully logged in!",
#         "use_menu": "Use menu items to navigate.",
#         "yes": "Yes",
#         "no": "No"
#     },
#     "reg": {
#         "user_registered": "This user is already registered!",
#         "em_for_reg": "Enter your email to register.",
#         "pass_for_reg": "Enter your password to register",
#         "success_up": "You have successfully registered!\n\nNow you can log in!",
#         "cancel": "Cancel registration"
#     },
#     "unsafe_pass": {
#         "mes_unsafe_pass": "The password you entered is not secure.\n\nWe recommend adding:\n\n",
#         "lower_symb": "Lower case symbols.\n\n",
#         "upper_symb": "Uppercase symbols.\n\n",
#         "numbes": "Numbers.\n\n",
#         "special_symb": "Special symbols."
#     },
#     "client_menu": {
#         "account": "Account",
#         "cont_panel": "Control Panel",
#         "crypto_rate": "Crypto rates",
#         "message": "You are in the control panel."
#     },
#     "acc_settings": {
#         "security": "Security",
#         "logout": "Logout",
#         "referal": "Referral program",
#         "support": "Support",
#         "back": "Back",
#         "message": "You are in your account settings.."
#     },
#     "secure": {
#         "change_pass": "Change password",
#         "change_email": "Change Email",
#         "two_auth": "Two-factor authentication",
#         "acc_activity": "Account Activity"
#     }
# }

write_to_json(data, r"languages/ru/ru.json")
write_to_json(messages, r"languages/ru/ru_messages.json")