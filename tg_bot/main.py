import mysql.connector

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

dbConfig = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'wecan'
}
maxTries = 10
cursor = None

BEGINMSG = "Hi. Welcome to Wecan. "

def start(update, context):
    update.message.reply_text(BEGINMSG)

def main():
    global cursor
    updater = Updater("1275114481:AAEcU0WoAkjzN-1Pv-UPp9qnpOPdrNwOQrE", use_context=True)
    dp = updater.dispatcher
    while True:
        try:
            connection = mysql.connector.connect(**dbConfig)
            cursor = connection.cursor()
            break
        except:
            print("Connection error")
            if maxTries > 0:
                time.sleep(2)
                maxTries = maxTries - 1
            else:
                exit(2)

    # Add Handlers
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
