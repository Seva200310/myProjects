
import requests
import json
import time
import Chekist
# -*- coding: utf-8 -*-
import telebot
token="токена нет"
ID="ID нет"
       
bot = telebot.TeleBot("1804574146:AAHZldDw8ARfyHTPGW3O8L41FkTBx6kJMkQ")
@bot.message_handler(content_types=["text"])


def handle_text(message):   
    def idRequest(message):
     global ID
     if message.text:
       ID=message.text
       bot.send_message(message.from_user.id,ID)
       handle_text(message)
       Params={}
       Params["token"]=token
       Params["userId"]=ID
       userinfo=Chekist.searchHiddenFriendsAndMentions(Params)
       arrHiddenFriends=userinfo["hiddenFriends"]
       arrHFinfo=[]
       for item in arrHiddenFriends:
        hf=item
        hfInfo="\nИмя:"+str(hf["name"])+"\nФамилия:"+str(hf["surname"])+"\nСтраница:"+str(hf["link"])+""
        arrHFinfo.append(hfInfo)
       allHFinfoString="".join(arrHFinfo)
        
       messageResult="Имя:"+str(userinfo["name"])+"\nФамилия:"+str(userinfo["surname"])+"\nID:"+str(userinfo["userId"])+"\nУпоминания в комментариях:"+str(userinfo["mentions"])+"\nСкрытые Друзья:\n"+str(allHFinfoString)+""
       
       bot.send_message(message.from_user.id,messageResult)
    def tokenRequest(message):
     global token
     if message.text:
       token=message.text
       bot.send_message(message.from_user.id,token)
       msg = bot.send_message(chat_id, 'Теперь пришлите ID')
       bot.register_next_step_handler(msg,idRequest)
    if message.text == "Ты работаешь?":
        bot.send_message(message.from_user.id, "Работаю")
    elif message.text == "токен":
        bot.send_message(message.from_user.id, token)
    elif message.text == "Хочу инфу" or message.text == "Инфа":
         chat_id = message.chat.id
         text = message.text
         msg = bot.send_message(chat_id, 'Пришлите ваш токен вк')
         bot.register_next_step_handler(msg, tokenRequest)
         

    else:
        pass

bot.polling(none_stop=True, interval=0)


        
# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    handle_text(message)
    pass

 # Обработчик для документов и аудиофайлов
@bot.message_handler(content_types=['document', 'audio'])
def handle_document_audio(message):
    pass

bot.polling(none_stop=True, interval=0)  





