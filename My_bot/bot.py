import logging
from datetime import date

import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import setting
from random import randint, choice
from glob import glob
from emoji import emojize

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


# PROXY = {'proxy_url': settings.PROXY_URL,
#     'urllib3_proxy_kwargs': {
#         'username': settings.PROXY_USERNAME,
#         'password': settings.PROXY_PASSWORD
#     }
# }


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Привет, пользователь {context.user_data['emoji']}!")


def planet_from_ephem(update, context):
    # list_planet = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun')
    user_planet = update.message.text.split(' ')[1].title()
    print(user_planet)
    from_ephem = getattr(ephem, user_planet)
    # def from_ephem(planet):
    #     if planet == 'Mercury':
    #         return ephem.Mercury
    #     elif planet == 'Venus':
    #         return ephem.Venus
    #     elif planet == 'Earth':
    #         return ephem.Earth
    #     elif planet == 'Mars':
    #         return ephem.Mars
    #     elif planet == 'Jupiter':
    #         return ephem.Jupiter
    #     elif planet == 'Saturn':
    #         return ephem.Saturn
    #     elif planet == 'Uranus':
    #         return ephem.Uranus
    #     elif planet == 'Neptune':
    #         return ephem.Neptune
    #     elif planet == 'Pluto':
    #         return ephem.Pluto
    #     else:
    #         return ephem.Sun

    const = ephem.constellation(from_ephem(date.today()))[1]
    print(const)
    update.message.reply_text(f'Планета {user_planet} сегодня находится в созвездии {const}')


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"{user_text} {context.user_data['emoji']}")


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(setting.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выиграл!'
    return message


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            # message = f'Ваше число {user_number}'
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Введите целое число'

    else:
        message = 'Введите целое число'
    update.message.reply_text(message)


def send_cat_picture(update, context):
    cat_photos_list = glob('images/*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def main():
    mybot = Updater(setting.API_KEY, use_context=True)  # , request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("planet", planet_from_ephem))
    dp.add_handler(CommandHandler("cat", send_cat_picture))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
