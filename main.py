from bot import start_bot
import telebot
import sys

# here you need to set up target folders
message_path = sys.path[0]

# put your token to working folder
f = open(message_path + '/token.txt', 'r')
token = str(f.readline())

# Here start your chat bot
bot = telebot.TeleBot(token, parse_mode=None)

# is the function you need to put in message handler block in your chatbot
start_bot(bot, message_path)


# here you can setup your password to stop collecting data
@bot.message_handler(commands=['password'])
def stop_command(message):
    print("the bot finished his job")
    bot.stop_polling()


bot.infinity_polling()

# if __name__ == '__main__':
