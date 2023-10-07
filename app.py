import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from reply_generator import classify_question


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("""
Привет!

Я могу проконсультировать тебя как называется трава на латыни
Просто спроси!
    """, parse_mode=telegram.ParseMode.MARKDOWN)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
Я могу проконсультировать тебя как называется трава на латыни
Просто спроси!
    """, parse_mode=telegram.ParseMode.MARKDOWN)


def echo(update, context):
    """Echo the user message."""
    answer = classify_question(update.message.text)

    dump_data(update.message.from_user, update.message.text, answer)

    update.message.reply_text(answer)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def dump_data(user, question, answer):
    username = user.username
    full_name = user.full_name
    id = user.id

    str = """{username}\t{full_name}\t{id}\t{question}\t{answer}\n""".format(username=username,
                                                                             full_name=full_name,
                                                                             id=id,
                                                                             question=question,
                                                                             answer=answer)

    with open("dump.tsv", "a") as myfile:
        myfile.write(str)


def get_answer():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("6449951395:AAFwMEtnK9ueWrR8PgfGS1-5f0uwR4FENSA", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    get_answer()
