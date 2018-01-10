#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from uuid import uuid4

import re

from telegram.utils.helpers import escape_markdown
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove	
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler,CallbackQueryHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    name=update['message']['chat']['first_name']
    name=name.encode('utf-8')
    hitext='Hi '+name+'! Add me to a group or use the bot inline to play!'
    update.message.reply_text(hitext)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help section will be updated soon!')


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    if not query:
        return
    start_user=update.inline_query.from_user.username
    #start_user=update['from']['username']
    start_user=start_user.encode('utf-8')
    
    start_keyboard = [[InlineKeyboardButton("Join Game", callback_data='join')]]
    start_markup = InlineKeyboardMarkup(start_keyboard)
    
    #init_text='Waiting for playerssss	:\n'+start_user	
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Start Game!",
            input_message_content=InputTextMessageContent('Game started by:\n@{}\nWaiting for player..'.format(start_user)),
            reply_markup=start_markup)
            
        ]

    update.inline_query.answer(results)

def startbutton(bot, update):	
    query = update.callback_query	
    #print query
    
    toss_keyboard = [[  InlineKeyboardButton("1", callback_data='1'),
                 		InlineKeyboardButton("2", callback_data='2'),
                 		InlineKeyboardButton("3", callback_data='3'),
                 		InlineKeyboardButton("4", callback_data='4'),
                 		InlineKeyboardButton("5", callback_data='5'),
                 		InlineKeyboardButton("6", callback_data='6')
                    ]]
                
    toss_markup = ReplyKeyboardMarkup(toss_keyboard)
    #reply_markup=ReplyKeyboardMarkup(toss_keyboard, one_time_keyboard=True)
    bot.edit_message_text(text="ODD OR EVEN:\n Perform toss\n Click on any of the buttons below:", chat_id=None,message_id=None, inline_message_id = query.inline_message_id)
     
              	

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("361601866:AAFrx5ErLFGhfUb1nCGmvGINShkubObGWO8")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(startbutton))
    

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main()
