# Импортируем нужные компаненты
from emoji import emojize
from glob import glob 
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

# Запись отчета о работе бота
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Настройки прокси
PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}

def greet_user(update, context):
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!")

# Функция которая отвечает пользователю
def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(f"{user_text} {context.user_data['emoji']}")

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, мое {bot_number}. Вы выйграли.'
    elif user_number == bot_number:
        message = f'Ваше число {user_number}, мое {bot_number}. Ничья.'
    else:
        message = f'Ваше число {user_number}, мое {bot_number}. Я выйграл.'
    return message

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            messege = play_random_numbers(user_number)
        except(ValueError, Exception):
            messege = 'Введите целое число'  
    else:
        messege = 'Введите число'
    update.message.reply_text(messege)

def send_cat_picture(update, context):
    cat_globo_list = glob('image/cat*.jp*g')
    cat_photo_filename = choice(cat_globo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))

# Функция, которая соединяется с плтформой Telegrem, 'тело' бота
def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user)) # добавление диспетчеру обработчик, который реагирует на страт и вызывае greet_user
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
