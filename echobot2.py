#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import json
from requests.auth import HTTPBasicAuth

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Functions to interact with awattgarde API
def getUserInformation(user, password):
    response = requests.get('http://vkw.demo.ben-energy.com/api/v2/rest/Customer.json?Email='+user+'&token=c854c5371b84a30c8a459870189bd81a', auth=HTTPBasicAuth(user, password))
    data = json.loads(response.text)
    surname = data["items"][0]["Surname"]
    return surname

def getTips(user, password):
   
    response = requests.get('https://vkw.demo.ben-energy.com/api/v2/service/SavingTipWebService/getTips?token=c854c5371b84a30c8a459870189bd81a&status=promised', auth=HTTPBasicAuth(user, password))
    data = json.loads(response.text)
    promised = data["response"]["promised"]
    output = promised
    #output = "Promised tips: "
    #for tip in promised:
    #    output += tip["Title"] +" "
    return output

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def login(bot, update):
    data = getUserInformation('tobias.graml@ben-energy.com','123456')
    update.message.reply_text(data + " logged in")

def tips(bot, update):
    output = getTips('tobias.graml@ben-energy.com','123456')
    #update.message.reply_text(output)
    keyboard = []
    for tip in ouput:
        #output += tip["Title"] +" "
        keyboard = keyboard.append([InlineKeyboardButton(tip["Title"], callback_data=tip["ID"])])

    keyboard = keyboard.append([InlineKeyboardButton("Nichts", callback_data=0)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hast du etwas erledigt?:', reply_markup=reply_markup)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("401178199:AAEYNJd-GZTUANZMyC3MRcU6_nlKxBhXBXw")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("login", login))
    dp.add_handler(CommandHandler("tips", tips))

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


if __name__ == '__main__':
    main()