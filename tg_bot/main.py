import mysql.connector
import logging
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode

from db_manage import check_username_exists, check_login, fetch_boards_of, create_board_in_db, check_board_exists, check_card_exists
from db_manage import get_board_name_by_id, create_list_in_db, fetch_lists_of, check_list_exists, get_list_name_by_id, fetch_cards_of, fetch_card, fetch_pending_deadlines

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

USERNAME, PASSWORD, LOGGED_IN, CHOOSING_BOARDS, CREATE_BOARD_ID, CHOOSING_BOARD_ACTION, CREATE_LIST_GET_LABEL, CREATE_LIST_ID, CHOOSING_LISTS, CHOOSING_LIST_ACTION, CHOOSING_CARDS, CHOOSING_CARD_ACTION = range(12)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

def exit_board(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data):
        del context.user_data['board_id']
        logged_in_state(update, context)
        return LOGGED_IN
    else:
        logout(update, context)
        return ConversationHandler.END

def exit_list(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data and
        'list_id' in context.user_data):
        del context.user_data['list_id']
        choose_board_action(update, context)
        return CHOOSING_BOARD_ACTION
    else:
        logout(update, context)
        return ConversationHandler.END

def exit_card(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data and
        'list_id' in context.user_data and
        'card_id' in context.user_data):
        del context.user_data['card_id']
        choose_list_action(update, context)
        return CHOOSING_LIST_ACTION
    else:
        logout(update, context)
        return ConversationHandler.END
    
def choose_board_action(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data):
        try:
            update.message.reply_text(
                f"Choose action for board: {get_board_name_by_id(context.user_data['board_id'])}",
                reply_markup = ReplyKeyboardMarkup(
                    [["Show Lists"], ["Create List"], ["Go Back to Main Menu"]],
                    resize_keyboard = True
                )
            )
            return CHOOSING_BOARD_ACTION
        except:
            update.message.reply_text("Wrong action")
            logout(update, context)
            return ConversationHandler.END
    else:
        update.message.reply_text("Inappropriate action")
        logout(update, context)
        return ConversationHandler.END

def choose_list_action(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data and
        'list_id' in context.user_data):
        try:
            update.message.reply_text(
                f"Choose action for list: {get_list_name_by_id(context.user_data['list_id'])}",
                reply_markup = ReplyKeyboardMarkup(
                    [["Show Cards"], ["Create Card"], ["Go Back to Board"]],
                    resize_keyboard = True
                )
            )
            return CHOOSING_LIST_ACTION
        except:
            update.message.reply_text("Wrong action")
            logout(update, context)
            return ConversationHandler.END
    else:
        update.message.reply_text("Inappropriate action")
        logout(update, context)
        return ConversationHandler.END

def choose_card_action(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data and
        'list_id' in context.user_data and
        'card_id' in context.user_data):
        try:
            card_name, card_text, comments = fetch_card(context.user_data['card_id'])
            response_text = (
                f"*{card_name}*\n\n" +
                f"{card_text}\n\n*Comments*:\n" +
                "\n\n".join(["__" + x[0] + "__" + ": " + x[1] for x in comments])
            )
            update.message.reply_text(
                response_text,
                reply_markup = ReplyKeyboardMarkup(
                    [["Go Back to List"]],
                    resize_keyboard = True
                ),
                parse_mode = ParseMode.MARKDOWN
            )
            return CHOOSING_CARD_ACTION
        except:
            update.message.reply_text("Wrong action")
            logout(update, context)
            return ConversationHandler.END
    else:
        update.message.reply_text("Inappropriate action")
        logout(update, context)
        return ConversationHandler.END


def logged_in_state(update, context):
    update.message.reply_text(
        "Choose action",
        reply_markup = ReplyKeyboardMarkup(
            [['Show boards'], ['Show pending deadlines'], ['Create Board'], ['logout']],
            resize_keyboard=True
        ),
    )
    return LOGGED_IN
    
def start(update, context):
    update.message.reply_text(
        BEGINMSG,
        reply_markup = ReplyKeyboardMarkup(
            [['/login']],
            one_time_keyboard=True,
            resize_keyboard=True
        ),
    )

def callback_queries(update, context):
    card_id_filter = re.compile("CARD_ID\:([0-9]*)")
    query = update.callback_query
    if match:=card_id_filter.search(query.data):
        card_id = match.group(1)
        print(card_id)
        query.answer()
        card_name, card_text, comments = fetch_card(card_id)
        response_text = (
            f"*{card_name}*\n\n" +
            f"{card_text}\n\n*Comments*:\n" +
            "\n\n".join(["__" + x[0] + "__" + ": " + x[1] for x in comments])
        )
        query.edit_message_text(response_text, parse_mode = ParseMode.MARKDOWN)
    else:
        query.answer()
        
def create_board(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data):
        update.message.reply_text(
            "Type board name",
            reply_markup=ReplyKeyboardRemove()
        )
        return CREATE_BOARD_ID
    else:
        logout(update, context)
        return ConversationHandler.END

def create_list(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data):
        update.message.reply_text(
            "Type list name",
            reply_markup=ReplyKeyboardRemove()
        )
        return CREATE_LIST_GET_LABEL
    else:
        logout(update, context)
        return ConversationHandler.END

def create_card(update, context):
    pass

def create_list_label(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data):
        pattern = re.compile("[0-9A-Za-z]*")
        if pattern.fullmatch(update.message.text):
            context.user_data['list_name'] = update.message.text
            update.message.reply_text(
                "Enter label for list",
                reply_markup=ReplyKeyboardRemove()
            )
            return CREATE_LIST_ID
        else:
            update.message.reply_text(
                "Enter appropriate name",
                reply_markup=ReplyKeyboardRemove()
            )
            return CREATE_LIST_GET_LABEL
    else:
        logout(update, context)
        return ConversationHandler.END
    
def create_board_id(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data):
        pattern = re.compile("[0-9A-Za-z]*")
        if match := pattern.fullmatch(update.message.text):
            try:
                if create_board_in_db(context.user_data['username'], match.group(0)):
                    update.message.reply_text("Board created succefully")
                else:
                    update.message.reply_text("The board could not be created")
            except:
                update.message.reply_text("There was an error in creating the board")
            logged_in_state(update, context)
            return LOGGED_IN
        else:
            update.message.reply_text("Please enter appropriate name")
            return CREATE_BOARD_ID
    else:
        logout(update, context)
        return ConversationHandler.END

def create_list_id(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data and
        'list_name' in context.user_data):
        pattern = re.compile("[0-9A-Za-z]*")
        if match := pattern.fullmatch(update.message.text):
            try:
                if create_list_in_db(context.user_data['username'], context.user_data['board_id'], context.user_data['list_name'], match.group(0)):
                    update.message.reply_text("List created succefully")
                else:
                    update.message.reply_text("The list could not be created")
            except:
                update.message.reply_text("There was an error in creating the list")
            del context.user_data['list_name']
            choose_board_action(update, context)
            return CHOOSING_BOARD_ACTION
        else:
            update.message.reply_text("Please enter appropriate name")
            return CREATE_LIST_ID
    else:
        logout(update, context)
        return ConversationHandler.END

def show_list(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data):
        lists = fetch_lists_of(context.user_data['board_id'], context.user_data['username'])
        if len(lists) > 0:
            update.message.reply_text(
                "Select a list, or press \"Go Back\"",
                #reply_markup=reply_markup
                reply_markup = ReplyKeyboardMarkup(
                    [[x[1] + ":" + str(x[0])] for x in lists] + [["Go Back"]],
                    one_time_keyboard=True,
                    resize_keyboard=True
                )
            )
            return CHOOSING_LISTS
        else:
            update.message.reply_text("No Lists available!")
            choose_board_action(update, context)
            return CHOOSING_BOARD_ACTION
    else:
        logout(update, context)
        return ConversationHandler.END

def show_cards(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data and
        'list_id' in context.user_data):
        cards = fetch_cards_of(context.user_data['username'], context.user_data['board_id'], context.user_data['list_id'])
        if len(cards) > 0:
            update.message.reply_text(
                "Select a card, or press \"Go Back\"",
                reply_markup = ReplyKeyboardMarkup(
                    [[x[1] + ":" + str(x[0])] for x in cards] + [["Go Back"]],
                    one_time_keyboard=True,
                    resize_keyboard=True
                )
            )
            return CHOOSING_CARDS
        else:
            update.message.reply_text("No Lists available!")
            choose_list_action(update, context)
            return CHOOSING_LIST_ACTION
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
                "Select a board, or press \"Go Back\"",
                #reply_markup=reply_markup
                reply_markup = ReplyKeyboardMarkup(
                    [[x[1] + ":" + str(x[0])] for x in boards] + [["Go Back"]],
                    one_time_keyboard=True,
                    resize_keyboard=True
                )
            )
            return CHOOSING_BOARDS
        else:
            update.message.reply_text("No Boards available!")
            logged_in_state(update, context)
            return LOGGED_IN
    else:
        logout(update, context)
        return ConversationHandler.END

def show_pending_deadlines(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data):
        pending_deadlines = fetch_pending_deadlines(context.user_data['username'])
        print(pending_deadlines)
        if len(pending_deadlines) > 0:
            deadline_keys = map(lambda x: [InlineKeyboardButton(x[1] + " " + str(x[2]), callback_data=("CARD_ID:" + str(x[0])))], pending_deadlines)
            reply_markup = InlineKeyboardMarkup(deadline_keys)
            update.message.reply_text(
                "Your pending deadlines",
                #reply_markup=reply_markup
                reply_markup = reply_markup
            )
            return LOGGED_IN
        else:
            update.message.reply_text("No Pending deadlines! Hurray")
            logged_in_state(update, context)
            return LOGGED_IN
    else:
        logout(update, context)
        return ConversationHandler.END
    
def select_list(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data):
        pattern = re.compile('^([^\:]*)\:([0-9]*)$')
        if match := pattern.fullmatch(update.message.text):
            list_name = match.group(1)
            list_id = match.group(2)
            if check_list_exists(context.user_data['board_id'], context.user_data['username'], list_name, list_id):
                update.message.reply_text(f"You are in List: {list_name}")
                context.user_data['list_id'] = f"{list_id}"
                choose_list_action(update, context)
                return CHOOSING_LIST_ACTION
            else:
                show_list(update, context)
                return CHOOSING_LISTS
        else:
            update.message.reply_text("Please enter something appropriate")
            choose_board_action(update, context)
            return CHOOSING_BOARD_ACTION
    else:
        logout(update, context)
        return ConversationHandler.END

def select_card(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data and
        'board_id' in context.user_data and
        'list_id' in context.user_data):
        pattern = re.compile('^([^\:]*)\:([0-9]*)$')
        if match := pattern.fullmatch(update.message.text):
            card_name = match.group(1)
            card_id = match.group(2)
            if check_card_exists(context.user_data['username'], context.user_data['board_id'], context.user_data['list_id'], card_id, card_name):
                update.message.reply_text(f"You are in Card: {card_name}")
                context.user_data['card_id'] = f"{card_id}"
                choose_card_action(update, context)
                return CHOOSING_CARD_ACTION
            else:
                show_cards(update, context)
                return CHOOSING_CARDS
        else:
            update.message.reply_text("Please enter something appropriate")
            choose_list_action(update, context)
            return CHOOSING_LIST_ACTION
    else:
        logout(update, context)
        return ConversationHandler.END

def select_board(update, context):
    if ('state' in context.user_data and
        context.user_data['state'] == 'logged_in' and
        'username' in context.user_data):
        pattern = re.compile('^([^\:]*)\:([0-9]*)$')
        if match := pattern.fullmatch(update.message.text):
            board_name = match.group(1)
            board_id = match.group(2)
            if check_board_exists(board_name, board_id, context.user_data['username']):
                update.message.reply_text(f"You are in Board: {board_name}")
                context.user_data['board_id'] = f"{board_id}"
                choose_board_action(update, context)
                return CHOOSING_BOARD_ACTION
            else:
                show_boards(update, context)
                return CHOOSING_BOARDS
        else:
            update.message.reply_text("Please enter something appropriate")
            logged_in_state(update, context)
            return LOGGED_IN
    else:
        logout(update, context)
        return ConversationHandler.END
        
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
    context.user_data.clear()
    # del context.user_data['state']
    # del context.user_data['username']
    # del context.user_data['board_id']
    start(update, context)
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
                MessageHandler(Filters.regex('^(Show boards)$'), show_boards),
                MessageHandler(Filters.regex('^(logout)$'), logout),
                MessageHandler(Filters.regex('^(Create Board)$'), create_board),
                MessageHandler(Filters.regex('^(Show pending deadlines)$'), show_pending_deadlines)
            ],
            CREATE_BOARD_ID: [MessageHandler(Filters.text, create_board_id)],
            CHOOSING_BOARDS: [
                MessageHandler(Filters.regex('^[^\:]*\:[0-9]*$'), select_board),
                MessageHandler(Filters.regex('^(Go Back)$'), logged_in_state)
            ],
            CHOOSING_BOARD_ACTION: [
                MessageHandler(Filters.regex('^(Go Back to Main Menu)$'), exit_board),
                MessageHandler(Filters.regex('^(Create List)$'), create_list),
                MessageHandler(Filters.regex('^(Show Lists)$'), show_list)
            ],
            CHOOSING_LIST_ACTION: [
                MessageHandler(Filters.regex('^(Go Back to Board)$'), exit_list),
                MessageHandler(Filters.regex('^(Create Card)$'), create_card),
                MessageHandler(Filters.regex('^(Show Cards)$'), show_cards)
            ],
            CREATE_LIST_GET_LABEL: [MessageHandler(Filters.text, create_list_label)],
            CREATE_LIST_ID: [MessageHandler(Filters.text, create_list_id)],
            CHOOSING_LISTS: [
                MessageHandler(Filters.regex('^[^\:]*\:[0-9]*$'), select_list),
                MessageHandler(Filters.regex('^(Go Back)$'), choose_board_action)
            ],
            CHOOSING_CARDS: [
                MessageHandler(Filters.regex('^[^\:]*\:[0-9]*$'), select_card),
                MessageHandler(Filters.regex('^(Go Back)$'), choose_list_action)
            ],
            CHOOSING_CARD_ACTION: [
                MessageHandler(Filters.regex('^(Go Back to List)$'), exit_card),
            ],
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
