#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters, BaseFilter

from sapper import init_sapper, answer, clear
import telegram
from telegram import Update, ForceReply

token = '5281554471:AAFzRHww-Y3PvZ1Ji-B-XiHbTBPbqKnPWNI'
bot = telegram.Bot(token)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        'Привет! Чтобы начать игру, введи /game. Чтобы узнать правила, введи /rules'
    )


def rules(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        'В игре есть поле 5 на 5. Там спрятаны 10 мин. '
        'У вас есть 15 ходов, чтобы найти как можно больше мин. Очки между играми суммируются. '
        'для каждого хода введите букву(строка) и число(колонка). '
        'Можно вводить несколько ходов одновременно, разделяя их запятыми.'
        'Наберите как можно больше очков, чтобы попасть в рейтинг!'
    )


def game(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        init_sapper(user.id)
    )


def process_answer(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        answer(user.id, update.message.text)
    )



def clear_process(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    clear(user.id)
    update.message.reply_html(
        'Достижения обнулены! у вас 0 очков.'
    )


def main() -> None:
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("game", game))
    dispatcher.add_handler(CommandHandler("clear", clear_process))
    dispatcher.add_handler(CommandHandler("rules", rules))
    dispatcher.add_handler(MessageHandler(Filters.regex('([a-eA-E][1-5][, ]*){1,10}'), process_answer))
    dispatcher.add_handler(MessageHandler(Filters.all, start))

    # Start the Bot
    updater.start_polling()
    updater.idle()


main()