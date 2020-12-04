import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import telebot
import telegram
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from codes import A

bot = telebot.TeleBot(A.code)

def send_email(addr_to, msg_subj, msg_text, files=None):
    # files = {'Как назвать': 'Где лежит'}
    addr_from = "a.alex.2000@mail.ru"  # Отправитель
    password = "Bah78upr"  # Пароль

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = msg_subj  # Тема сообщения

    body = msg_text  # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    if files:
        for x, y in files.items():
            try:
                ctype, encoding = mimetypes.guess_type(y)  # Определяем тип файла на основе его расширения
                if ctype is None or encoding is not None:  # Если тип файла не определяется
                    ctype = 'application/octet-stream'  # Будем использовать общий тип
                maintype, subtype = ctype.split('/', 1)
                fp = open(y, 'rb')
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
                file.add_header('Content-Disposition', 'attachment', filename=x)  # Добавляем заголовки
                msg.attach(file)
            except Exception as ex:
                print(ex)

    # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================
    # server = smtplib.SMTP_SSL('*****yandex.ru', 465)        # Создаем объект SMTP
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    # server.starttls()                                      # Начинаем шифрованный обмен по TLS
    # server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()


def mk(d: list, t=1):
    keyboard = ReplyKeyboardMarkup(row_width=t)
    for name in d:
        keyboard.add(KeyboardButton(name))
    return keyboard


def make_keyboard(d: dict, k=1):
    keyboard = InlineKeyboardMarkup(row_width=k)
    for name, call in d.items():
        keyboard.row(InlineKeyboardButton(name, callback_data=call))
    return keyboard


def send_m(who, text):
    s = bot.send_message(chat_id=who, text=text, parse_mode=telegram.ParseMode.HTML)
    return s


def send_d(who, text, t=''):
    with open(text, 'rb') as f:
        bot.send_document(who, f, caption=t)


def send_ph(who, photo):
    bot.send_photo(who, photo)


def edit(who, txt, button, mes):
    bot.edit_message_text(txt, chat_id=who, message_id=mes.message_id, reply_markup=mk(button))


def sm(who, text, button):
    bot.send_message(who, text, reply_markup=make_keyboard(button), parse_mode=telegram.ParseMode.HTML)


def kl(who, text, button):
    bot.send_message(who, text, reply_markup=mk(button), parse_mode=telegram.ParseMode.HTML)


def ch(who, txt, button, mes):
    bot.edit_message_text(txt, chat_id=who, message_id=mes.message_id, reply_markup=make_keyboard(button),
                          parse_mode=telegram.ParseMode.HTML)