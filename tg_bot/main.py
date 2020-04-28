import mysql.connector
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler

from telegram import ReplyKeyboardMarkup
from telegram import ParseMode

from db_manage import check_username_exists, check_login

dbConfig = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    #'host': 'localhost',
    'port': '3306',
    #'port': '32000',
    'database': 'wecan'
}
maxTries = 20
connection = ""
cursor = None

BEGINMSG = "Hi. Welcome to Wecan. Send \
/login to begin login process."

USERNAME, PASSWORD, LOGGED_IN = range(3)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        BEGINMSG,
        reply_markup = ReplyKeyboardMarkup(
            [['/login']],
            one_time_keyboard=True
        )
    )

def show_boards(update, context):
    pass
    
def login(update, context):
    update.message.reply_text("Type username")
    return USERNAME

def cancel(update, context):
    pass

def username(update, context):
    username = update.message.text
    username_exists = check_username_exists(username)
    if username_exists:
        context.user_data['state'] = "username_verified"
        context.user_data['username'] = username
        update.message.reply_text("Enter password")
        return PASSWORD
    update.message.reply_text("Bad username. Aborting")
    return ConversationHandler.END
    
def password(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == "username_verified"):
        password = update.message.text
        if check_login(context.user_data['username'], password):
            update.message.reply_text("Succefully logged in. Hurray")
            return LOGGED_IN
        else:
            update.message.reply_text("Wrong password")
            return ConversationHandler.END
    else:
        update.message.reply_text("Use /login, to login")
        return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
def main():
    global cursor, connection
    updater = Updater("1275114481:AAEcU0WoAkjzN-1Pv-UPp9qnpOPdrNwOQrE", use_context=True)
    dp = updater.dispatcher
    
    # Add Handlers
    dp.add_handler(CommandHandler("start", start))

    login_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login)],
        states={
            USERNAME: [MessageHandler(Filters.text, username)],
            PASSWORD: [MessageHandler(Filters.text, password)],
            LOGGED_IN: [
                CommandHandler('show_boards', show_boards)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(login_handler)

    # log all errors
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
