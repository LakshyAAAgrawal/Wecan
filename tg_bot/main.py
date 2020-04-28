import mysql.connector
import logging
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode

from db_manage import check_username_exists, check_login, fetch_boards_of, create_board_in_db

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

USERNAME, PASSWORD, LOGGED_IN, CHOOSING_BOARDS, CREATE_BOARD_ID = range(5)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

def logged_in_state(update, context):
    update.message.reply_text(
        "Choose action",
        reply_markup = ReplyKeyboardMarkup(
            [['Show boards'], ['logout']],
            one_time_keyboard=True
        )
    )
    
def start(update, context):
    update.message.reply_text(
        BEGINMSG,
        reply_markup = ReplyKeyboardMarkup(
            [['/login']],
            one_time_keyboard=True
        )
    )

def create_board(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data):
        update.message.reply_text(
            "Type board_name",
            reply_markup=ReplyKeyboardRemove()
        )
        return CREATE_BOARD_ID
    else:
        logout(update, context)
        return ConversationHandler.END

def create_board_id(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data):
        pattern = re.compile("[0-9A-Za-z]")
        if match := pattern.fullmatch(update.message.text):
            create_board_in_db(context.user_data['username'], match.group(0))
    else:
        logout(update, context)
        return ConversationHandler.END

def show_boards(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data):
        boards = fetch_boards_of(context.user_data['username'])
        if len(boards) > 0:
            board_keys = map(lambda x: [InlineKeyboardButton(x[1], callback_data=("BOARD_ID:" + str(x[0])))], boards)
            reply_markup = InlineKeyboardMarkup(board_keys)
            update.message.reply_text(
                "Your Boards:",
                reply_markup=reply_markup
            )
            return LOGGED_IN
        else:
            update.message.reply_text("No Boards available!")
            logged_in_state(update, context)
            return LOGGED_IN
    else:
        logout(update, context)
        return ConversationHandler.END

def select_board(update, context):
    update.message.reply_text(update.message.text)
    pass

def login(update, context):
    update.message.reply_text(
        "Type username",
        reply_markup=ReplyKeyboardRemove()
    )
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
    start(update, context)
    return ConversationHandler.END

def password(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == "username_verified"):
        password = update.message.text
        if check_login(context.user_data['username'], password):
            update.message.reply_text("Succefully logged in. Hurray")
            context.user_data['state'] = "logged_in"
            logged_in_state(update, context)
            return LOGGED_IN
        else:
            update.message.reply_text("Wrong password")
            del context.user_data['state']
            del context.user_data['username']
            start(update, context)
            return ConversationHandler.END
    else:
        update.message.reply_text("Use /login, to login")
        start(update, context)
        return ConversationHandler.END

def logout(update, context):
    del context.user_data['state']
    del context.user_data['username']
    start(update, context)
    return ConversationHandler.END
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def callback_queries(update, context):
    pattern = re.compile("BOARD_ID\:([0-9]*)")
    query = update.callback_query
    if match:=pattern.search(query.data):
        board_id = match.group(1)
        print(board_id)
        query.answer()
        context.bot.send_message(, "Selected option: {}".format(query.data))
    
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
                MessageHandler(Filters.regex('^(Show boards)$'), show_boards),
                MessageHandler(Filters.regex('^(logout)$'), logout),
                MessageHandler(Filters.regex('^(Create Board)$'), create_board),
                MessageHandler(Filters.regex('^BOARD_ID\:[0-9]*$'), select_board)
            ],
            CREATE_BOARD_ID: [MessageHandler(Filters.text, create_board_id)]
        },
        fallbacks=[CommandHandler('cancel', logout)]
    )

    dp.add_handler(login_handler)
    dp.add_handler(CallbackQueryHandler(callback_queries))

    # log all errors
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
