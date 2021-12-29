# from threading import Thread
from bot import start_bot
import telebot

token = '5018142768:AAGZ0ysTkIi4dqP1tNdPhwZE1Vq8GrdhSFo'
# here you need to set up target folders
message_path = 'd:/_AI/work/ID_R&D/Telegram_bot/'

# Here start your chat bot
bot = telebot.TeleBot(token, parse_mode=None)

# is the function you need to put in message handler block in your chatbot
start_bot(bot, message_path)


@bot.message_handler(commands=['password'])
def stop_command(message):
    print("the bot finished his job")
    bot.stop_polling()


bot.infinity_polling()
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    print_hi('PyCharm')
#
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
