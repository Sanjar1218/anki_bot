from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import datetime
from database import *


def start(update, context):
    user_name = update.message.chat.username
    bot = context.bot
    chat_id = update.message.chat.id
    add_user(chat_id, user_name)
    button = ReplyKeyboardMarkup([['Create deck', 'My Decks']],
                                 resize_keyboard=True)
    bot.sendMessage(chat_id, 'test', reply_markup=button)


def my_decks(update, context):
    first = update.message.chat.first_name
    bot = context.bot
    chat_id = update.message.chat.id

    text = user_decks(chat_id)

    if len(text) == 1:
        button = KeyboardButton(str(text[0]))
        reply_markup = ReplyKeyboardMarkup([[button, 'Exit']],
                                           resize_keyboard=True)
        bot.sendMessage(chat_id,
                        'Which do you want to add',
                        reply_markup=reply_markup)
        return 'CHOICE'
    elif len(text) == 2:
        button = KeyboardButton(str(text[0]))
        button1 = KeyboardButton(str(text[1]))
        reply_markup = ReplyKeyboardMarkup([[button, button1], ['Exit']],
                                           resize_keyboard=True)
        bot.sendMessage(chat_id,
                        'Which do you want to add',
                        reply_markup=reply_markup)
        return 'CHOICE'
    elif len(text) == 3:
        button = KeyboardButton(str(text[0]))
        button1 = KeyboardButton(str(text[1]))
        button2 = KeyboardButton(str(text[2]))
        reply_markup = ReplyKeyboardMarkup(
            [[button, button1], [button2, 'Exit']], resize_keyboard=True)
        bot.sendMessage(chat_id,
                        'Which do you want to add',
                        reply_markup=reply_markup)
        return 'CHOICE'
    elif len(text) == 4:
        button = KeyboardButton(str(text[0]))
        button1 = KeyboardButton(str(text[1]))
        button2 = KeyboardButton(str(text[2]))
        button3 = KeyboardButton(str(text[3]))
        reply_markup = ReplyKeyboardMarkup(
            [[button, button1], [button2, button3], ['Exit']],
            resize_keyboard=True)
        bot.sendMessage(chat_id,
                        'Which do you want to add',
                        reply_markup=reply_markup)
        return 'CHOICE'
    elif len(text) >= 5:
        button = KeyboardButton(str(text[0]))
        button1 = KeyboardButton(str(text[1]))
        button2 = KeyboardButton(str(text[2]))
        button3 = KeyboardButton(str(text[3]))
        button4 = KeyboardButton(str(text[4]))
        reply_markup = ReplyKeyboardMarkup(
            [[button, button1], [button2, button3], [button4, 'Exit']],
            resize_keyboard=True)
        bot.sendMessage(chat_id,
                        'Which do you want to add',
                        reply_markup=reply_markup)
        return 'CHOICE'


def choose_deck(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    text = update.message.text

    change_dek(chat_id, text)

    button = ReplyKeyboardMarkup([['Read', 'Add to deck'], ['Exit']],
                                 resize_keyboard=True)
    bot.sendMessage(chat_id, 'Now begin to add word', reply_markup=button)
    return ConversationHandler.END


def create_deck(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    button = ReplyKeyboardMarkup([['Add to deck'], ['Exit']],
                                 resize_keyboard=True)
    bot.sendMessage(chat_id, 'What is the name of deck?', reply_markup=button)
    return 'DECK_NAME'


def deck_name(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    text = update.message.text

    change_dek(chat_id, text)
    # lst_add(chat_id, first)
    create_decks(chat_id, text)

    if text == 'Close':
        button = ReplyKeyboardMarkup([['Create deck', 'My Decks']],
                                     resize_keyboard=True)
        bot.sendMessage(chat_id, 'test', reply_markup=button)
        return ConversationHandler.END

    update.message.reply_text('Done, you can add now')
    return 'END'


def my_deck(update, context):
    bot = context.bot
    chat_id = update.message.chat.id

    minut = InlineKeyboardButton('<1m', callback_data='1')
    hour = InlineKeyboardButton('<10m', callback_data='10')
    day = InlineKeyboardButton('4d', callback_data='4')

    button = InlineKeyboardMarkup([[minut, hour, day]])

    bot.sendMessage(chat_id, 'laguages', reply_markup=button)


def alarm_minut(update, context):
    """Add a job to the queue."""
    print('minut')
    hour = 1

    update = update.callback_query
    chat_id = update.message.chat_id
    data = update.data

    print(data)

    deck_name = search_dek(chat_id)
    l = deck_end(chat_id, deck_name)
    x = search_user(chat_id)

    if data == 'a1':
        hour = 1
    elif data == 'a10':
        hour = 10

    lst = lst_back(chat_id, deck_name)
    timer(chat_id, x, deck_name)
    print(l, x)
    x += 1
    change_user(chat_id, x)

    context.job_queue.run_once(alarm,
                               datetime.timedelta(minutes=hour),
                               context={
                                   'deck_name': deck_name,
                                   'chat_id': chat_id
                               },
                               name='temp')
    if len(lst) == x + 1:
        print('munit if')
        change_user(chat_id, lst[x])
        button = InlineKeyboardButton('Hide', callback_data='hide')
        reply_markup = InlineKeyboardMarkup([[button]])
        update.edit_message_text('tugadi', reply_markup=reply_markup)
    else:
        text = deck_id_quest(lst[x], deck_name)
        button1 = InlineKeyboardButton('Show answer',
                                       callback_data='show_answer_time')
        button2 = InlineKeyboardButton('Exit', callback_data='Exit')
        button = InlineKeyboardMarkup([[button1, button2]])
        update.edit_message_text(text, reply_markup=button)


def show_alarm_answer(update, context):
    update = update.callback_query
    first = update.message.chat.id

    name = search_dek(first)
    x = search_user(first)

    # anki tabledagi so'zlar sonini qaytaradi
    # d = deck_end(name)
    # lst_tabledagi listni qaytaradi
    # lst = lst_back(first, name)

    quest = deck_id_quest(x, name)
    ans = deck_id_ans(x, name)

    minut = InlineKeyboardButton('<1m', callback_data='a1')
    hour = InlineKeyboardButton('<10m', callback_data='a10')
    day = InlineKeyboardButton('4d', callback_data='4')
    button1 = InlineKeyboardButton('Show answer',
                                   callback_data='show_answer_time')
    button2 = InlineKeyboardButton('Exit', callback_data='Exit')
    button = InlineKeyboardMarkup([[minut, hour, day], [button1, button2]])

    update.edit_message_text(f'{quest}\n-------\n{ans}', reply_markup=button)


def hide(update, context):
    update = update.callback_query
    #chat_id = update.message.chat.id
    #mes_id = update.message.message_id
    update.delete_message()


def begin(update, context):
    chat_id = update.message.chat.id

    change_user(chat_id, 1)
    name = search_dek(chat_id)
    # lst_up(first, name, 1)
    x = search_user(chat_id)
    text = deck_id_quest(x, name)

    button = InlineKeyboardButton('Show answer', callback_data='show_answer')
    button2 = InlineKeyboardButton('Exit', callback_data='Exit')
    reply_markup = InlineKeyboardMarkup([[button, button2]],
                                        resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup)


def alarm(context):
    """Send the alarm message."""
    job = context.job
    data = job.context
    name = job.name

    chat_id = data.get('chat_id', 123)
    deck_name = data.get('deck_name', 'ajoyib')

    x = search_user(chat_id)
    lst_id = times_up(chat_id, deck_name, name)
    # userning nechida qolib ketganini saqlab qoladi listning oxirida
    timer(chat_id, x, deck_name)

    # shu vaqtning ichida nima borligini va qaysi deck nomini qaytaradi
    # lst_id, deck_name = times_up()
    # userning ismiga bog'lab lst ni saqlab qoladi
    # lst_up(first, deck_name, lst)

    change_dek(chat_id, deck_name)
    change_user(chat_id, 0)
    deck_name = search_dek(chat_id)
    # agar lst bo'lsa ishlaydi bo'lmasa except ga o'tib ketadi

    x = search_user(chat_id)
    #change_user(first, x+1)
    print('alarmdagi', lst_id)
    text = deck_id_quest(lst_id[x], deck_name)
    # except:
    #     x = search_user(first)
    #     text = deck_id_quest(x, name)
    button1 = InlineKeyboardButton('Show answer',
                                   callback_data='show_answer_time')
    button2 = InlineKeyboardButton('Exit', callback_data='Exit')
    button = InlineKeyboardMarkup([[button1, button2]])
    context.bot.sendMessage(chat_id, text=text, reply_markup=button)


def minut(update, context):
    """Add a job to the queue."""
    update = update.callback_query
    chat_id = update.message.chat_id

    name = search_dek(chat_id)
    l = deck_end(chat_id, name)
    x = search_user(chat_id)

    # i dont know what is for this function
    # lst_back(first, name)

    timer(chat_id, x, name)
    x += 1
    change_user(chat_id, x)
    # print(l, x)
    context.job_queue.run_once(alarm,
                               datetime.timedelta(seconds=3),
                               context={
                                   'deck_name': name,
                                   'chat_id': chat_id
                               },
                               name='temp')
    if l == x - 1:
        print('munit if')
        button = InlineKeyboardButton('Hide', callback_data='hide')
        reply_markup = InlineKeyboardMarkup([[button]])
        update.edit_message_text('tugadi', reply_markup=reply_markup)
    else:
        text = deck_id_quest(x, name)

        button1 = InlineKeyboardButton('Show answer',
                                       callback_data='show_answer')
        button2 = InlineKeyboardButton('Exit', callback_data='Exit')
        button = InlineKeyboardMarkup([[button1, button2]])

        update.edit_message_text(text, reply_markup=button)


def minuts(update, context):
    """Add a job to the queue."""
    dt = datetime.datetime.today()
    update = update.callback_query
    chat_id = update.message.chat_id
    first = update.message.chat.first_name
    data = update.data

    name = search_dek(first)
    l = deck_end(first, name)
    x = search_user(first)
    hour = int(data)
    lst_back(first, name)

    # tank = tim(dt.year, dt.month, dt.day, dt.hour, dt.minute + hour, x, name)
    timer(dt.year, dt.month, dt.day, dt.hour, dt.minute + hour, x, name)
    x += 1
    change_user(first, x)
    print(l, x)
    # if tank:
    #     context.job_queue.run_once(alarm,
    #                                datetime.timedelta(minutes=hour),
    #                                context=chat_id,
    #                                name=str(first))
    if l == x - 1:
        print('munit if')
        button = InlineKeyboardButton('Hide', callback_data='hide')
        reply_markup = InlineKeyboardMarkup([[button]])
        update.edit_message_text('tugadi', reply_markup=reply_markup)
    else:
        text = deck_id_quest(x, first, name)

        button1 = InlineKeyboardButton('Show answer',
                                       callback_data='show_answer')
        button2 = InlineKeyboardButton('Exit', callback_data='Exit')
        button = InlineKeyboardMarkup([[button1, button2]])

        update.edit_message_text(text, reply_markup=button)


def show_answer(update, context):
    update = update.callback_query
    chat_id = update.message.chat.id

    name = search_dek(chat_id)
    x = search_user(chat_id)
    quest = deck_id_quest(x, name)
    ans = deck_id_ans(x, name)

    minut = InlineKeyboardButton('<1m', callback_data='temp')
    hour = InlineKeyboardButton('<10m', callback_data='box')
    day = InlineKeyboardButton('4d', callback_data='long')

    button1 = InlineKeyboardButton('Show answer', callback_data='show_answer')
    button2 = InlineKeyboardButton('Exit', callback_data='Exit')
    button = InlineKeyboardMarkup([[minut, hour, day], [button1, button2]])

    update.edit_message_text(f'{quest}\n-------\n{ans}', reply_markup=button)
    # <10m 4d 15d 29d


def day(update, context):
    """Add a job to the queue."""
    dt = datetime.datetime.today()
    update = update.callback_query
    chat_id = update.message.chat_id
    first = update.message.chat.first_name
    data = update.data
    name = search_dek(first)
    l = deck_end(first, name)
    x = search_user(first)
    hour = int(data)
    lst_back(first, name)

    tank = tim(dt.year, dt.month, dt.day + hour, dt.hour, dt.minute, x, name)
    timer(dt.year, dt.month, dt.day + hour, dt.hour, dt.minute, x, name)
    x += 1
    change_user(first, x)
    print(l, x)
    if tank:
        context.job_queue.run_once(alarm,
                                   datetime.timedelta(days=hour),
                                   context=chat_id,
                                   name=str(first))
    if l == x - 1:
        print('munit if')
        button = InlineKeyboardButton('Hide', callback_data='hide')
        reply_markup = InlineKeyboardMarkup([[button]])
        update.edit_message_text('tugadi', reply_markup=reply_markup)
    else:
        text = deck_id_quest(x, first, name)
        button1 = InlineKeyboardButton('Show answer',
                                       callback_data='show_answer')
        button2 = InlineKeyboardButton('Exit', callback_data='Exit')
        button = InlineKeyboardMarkup([[button1, button2]])
        update.edit_message_text(text, reply_markup=button)


def add(update, context):
    bot = context.bot
    chat_id = update.message.chat.id

    # search_user(first)
    button = ReplyKeyboardMarkup([['Close']], resize_keyboard=True)
    bot.sendMessage(chat_id, 'type question', reply_markup=button)
    return 'QUESTION'


def question(update, context):
    chat_id = update.message.chat.id
    text = update.message.text

    if text == 'Close':
        return close(update, context)

    path = search_dek(chat_id)
    quest(text, path)

    update.message.reply_text('Type answer')
    return 'ANSWER'


def answer(update, context):
    chat_id = update.message.chat.id
    text = update.message.text

    if text == 'Close':
        return close(update, context)

    path = search_dek(chat_id)
    ans(text, path)

    update.message.reply_text('Type question')
    return 'QUESTION'


def close(update, context):
    button = ReplyKeyboardMarkup([['Create deck', 'My Decks']],
                                 resize_keyboard=True)
    update.message.reply_text(
        'Thank you! Don\'t forget to memorized all of them',
        reply_markup=button)

    return ConversationHandler.END


def cancel(update, context):
    button = ReplyKeyboardMarkup([['Create deck', 'My Decks']],
                                 resize_keyboard=True)
    update.message.reply_text(
        'Thank you! Don\'t forget to memorized all of them',
        reply_markup=button)

    return ConversationHandler.END


updater = Updater(token='5297954693:AAGmz8OqL9EBPsfJ4S_R9AqgOtV67vkNtY4')
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(hide, pattern='hide'))
updater.dispatcher.add_handler(CallbackQueryHandler(minut, pattern='temp'))
updater.dispatcher.add_handler(CallbackQueryHandler(minuts, pattern='box'))
updater.dispatcher.add_handler(CallbackQueryHandler(day, pattern='long'))
updater.dispatcher.add_handler(
    CallbackQueryHandler(show_alarm_answer, pattern='show_answer_time'))
updater.dispatcher.add_handler(CallbackQueryHandler(alarm_minut, pattern='a1'))
updater.dispatcher.add_handler(CallbackQueryHandler(alarm_minut,
                                                    pattern='a10'))
updater.dispatcher.add_handler(
    CallbackQueryHandler(show_answer, pattern='show_answer'))
updater.dispatcher.add_handler(CallbackQueryHandler(close, pattern='Exit'))
updater.dispatcher.add_handler(MessageHandler(Filters.text('Exit'), close))
updater.dispatcher.add_handler(MessageHandler(Filters.text('Read'), begin))
updater.dispatcher.add_handler(
    MessageHandler(Filters.text('Show answer'), show_answer))

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text('Add to deck'), add)],
    states={
        'QUESTION': [MessageHandler(Filters.text, question)],
        'ANSWER': [MessageHandler(Filters.text, answer)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True)

chois = ConversationHandler(
    entry_points=[MessageHandler(Filters.text('My Decks'), my_decks)],
    states={
        'CHOICE': [MessageHandler(Filters.text, choose_deck)],
        'END': [MessageHandler(Filters.text('Close'), close)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True)

create_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.text('Create deck'), create_deck)],
    states={
        'DECK_NAME': [MessageHandler(Filters.text, deck_name)],
        'END': [MessageHandler(Filters.text('Close'), close)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True)

updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(chois)
updater.dispatcher.add_handler(create_conv)

updater.start_polling()
updater.idle()