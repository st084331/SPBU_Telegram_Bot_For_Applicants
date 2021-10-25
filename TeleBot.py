import telebot
import config
from telebot import types
from data import change_language, get_language, change_foreigner, get_foreigner, change_degree, get_degree
import model_ru_bac, model_mast, model_bac, model_asp, model_ru_asp, model_ru_mast, model_ru_ord, \
    model_ru_foreingner_mast, model_ru_foreingner_asp, model_ru_foreingner_bac
import json

with open('intents_bac.json') as file:
    data = json.load(file)
# Bot API
bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, config.Greating.format(message.from_user, bot.get_me()))
    select_language(message)


@bot.message_handler(commands=['language', 'start'])
def select_language(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    ENG_Button = types.InlineKeyboardButton("English", callback_data='ENG')
    RUS_Button = types.InlineKeyboardButton("Русский", callback_data='RUS')
    markup.add(ENG_Button, RUS_Button)
    bot.send_message(message.chat.id, "Please select a language\nПожалуйста, выберите язык", reply_markup=markup)


@bot.message_handler(commands=['status', 'start'])
def select_foreigner(message):
    if get_language(message.chat.id) == "RUS":
        markup2 = types.InlineKeyboardMarkup(row_width=2)
        Not_Foreigner = types.InlineKeyboardButton("Гражданин РФ", callback_data='NO')
        Foreigner = types.InlineKeyboardButton("Иностранец", callback_data='YES')
        markup2.add(Not_Foreigner, Foreigner)
        bot.send_message(message.chat.id, "Пожалуйста, выберите свой статус.", reply_markup=markup2)


@bot.message_handler(commands=['degree', 'start'])
def select_degree(message):
    markup3 = types.InlineKeyboardMarkup(row_width=3)
    if get_language(message.chat.id) == "ENG":
        Bachelor = types.InlineKeyboardButton("Bachelor", callback_data='Bachelor')
        Master = types.InlineKeyboardButton("Master", callback_data='Master')
        PhD = types.InlineKeyboardButton("Postgraduate", callback_data='PhD')
        Residency = types.InlineKeyboardButton("Residency", callback_data='Residency')
        markup3.add(Bachelor, Master, PhD, Residency)
        bot.send_message(message.chat.id, "Please select the degree of education you are interested in.",
                         reply_markup=markup3)
    elif get_language(message.chat.id) == "RUS":
        Bachelor = types.InlineKeyboardButton("Бакалавриат", callback_data='Bachelor')
        Master = types.InlineKeyboardButton("Магистратура", callback_data='Master')
        PhD = types.InlineKeyboardButton("Аспирантура", callback_data='PhD')
        Residency = types.InlineKeyboardButton("Ординатура", callback_data='Residency')
        markup3.add(Bachelor, Master, PhD, Residency)
        bot.send_message(message.chat.id, "Пожалуйста, выберите интересующую Вас степень образования.",
                         reply_markup=markup3)
    else:
        bot.send_message(message.chat.id, "Для начала выберите язык\nFirst select a language")
        select_language(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'ENG':
            bot.send_message(call.message.chat.id, 'Fine! To change the language, enter the command /language')
            bot.send_message(call.message.chat.id, "You can ask me any question that interests you!")
            change_language(call.message.chat.id, call.data, "YES", get_degree(call.message.chat.id))
            bot.edit_message_text(text="Please select a language", chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=None)
            if get_degree(call.message.chat.id) == "None":
                select_degree(call.message)
        elif call.data == 'RUS':
            bot.send_message(call.message.chat.id, 'Хорошо! Чтобы сменить язык, введите команду /language')
            change_language(call.message.chat.id, call.data, get_foreigner(call.message.chat.id),
                            get_degree(call.message.chat.id))
            bot.edit_message_text(text="Пожалуйста, выберите язык", chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=None)
            select_foreigner(call.message)
        elif call.data == "YES" or call.data == "NO":
            bot.send_message(call.message.chat.id, 'Хорошо! Чтобы сменить статус, введите команду /status')
            change_foreigner(call.message.chat.id, get_language(call.message.chat.id), call.data,
                             get_degree(call.message.chat.id))
            bot.edit_message_text(text="Пожалуйста, выберите свой статус.", chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=None)
            if get_degree(call.message.chat.id) == "None":
                select_degree(call.message)
        elif call.data == "Bachelor" or call.data == "Master" or call.data == "PhD" or call.data == "Residency":
            if get_language(call.message.chat.id) == "RUS":
                bot.send_message(call.message.chat.id,
                                 "Хорошо! Чтобы сменить интересующую степень образования, введите команду /degree")
                change_degree(call.message.chat.id, get_language(call.message.chat.id),
                              get_foreigner(call.message.chat.id),
                              call.data)
                bot.edit_message_text(text="Пожалуйста, выберите интересующую Вас степень образования.",
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id, reply_markup=None)
            elif get_language(call.message.chat.id) == "ENG":
                bot.send_message(call.message.chat.id,
                                 "Fine! To change the degree of education you are interested in, enter the command /degree")
                change_degree(call.message.chat.id, get_language(call.message.chat.id),
                              get_foreigner(call.message.chat.id),
                              call.data)
                bot.edit_message_text(text="Please select the degree of education you are interested in.",
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id, reply_markup=None)


@bot.message_handler(content_types=['text'])
def answers(message):
    if get_language(message.chat.id) == "ENG":
        if get_degree(message.chat.id) == "Bachelor":
            bot.send_message(message.chat.id, model_bac.chat_AI(message.text))
        if get_degree(message.chat.id) == "Master":
            bot.send_message(message.chat.id, model_mast.chat_AI(message.text))
        if get_degree(message.chat.id) == "PhD":
            bot.send_message(message.chat.id, model_asp.chat_AI(message.text))
        if get_degree(message.chat.id) == "Residency":
            bot.send_message(message.chat.id, "Sorry, I do not have information in English, so the level of education is for you.")
    elif get_language(message.chat.id) == "RUS":
        if get_foreigner(message.chat.id) == "NO":
            if get_degree(message.chat.id) == "Bachelor":
                bot.send_message(message.chat.id, model_ru_bac.chat_AI_ru(message.text))
            if get_degree(message.chat.id) == "Master":
                bot.send_message(message.chat.id, model_ru_mast.chat_AI_ru(message.text))
            if get_degree(message.chat.id) == "PhD":
                bot.send_message(message.chat.id, model_ru_asp.chat_AI_ru(message.text))
            if get_degree(message.chat.id) == "Residency":
                bot.send_message(message.chat.id, model_ru_ord.chat_AI_ru(message.text))
        elif get_foreigner(message.chat.id) == "YES":
            if get_degree(message.chat.id) == "Bachelor":
                bot.send_message(message.chat.id, model_ru_foreingner_bac.chat_AI_ru_foreingner(message.text))
            if get_degree(message.chat.id) == "Master":
                bot.send_message(message.chat.id, model_ru_foreingner_mast.chat_AI_ru_foreingner(message.text))
            if get_degree(message.chat.id) == "PhD":
                bot.send_message(message.chat.id, model_ru_foreingner_asp.chat_AI_ru_foreingner(message.text))
            if get_degree(message.chat.id) == "Residency":
                bot.send_message(message.chat.id, model_ru_ord.chat_AI_ru(message.text))


bot.polling(none_stop=True)
