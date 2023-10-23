import telebot
import time
from telebot import types
import requests
import json


token="5231562565:AAHG8c2bbvVOilEhD-Qdh3eEV4zhdJdMg3Q"
bot=telebot.TeleBot(token)
def json2arr(jsonObj):
      return json.loads(jsonObj.content)
def getLink(message):
    bot.send_photo(message.chat.id,photo=open('1.jpg','rb'))
    bot.send_photo(message.chat.id,photo=open('2.jpg','rb'))
    bot.send_message(message.chat.id,'Чтобы начать получать анонимные валентинки от своих друзей и знакомых, размести эту ссылку в любой соц.сети: https://t.me/Anonymess_bot?start='+str(message.chat.id)+' \n Важное примечание! Вы можете получить свою персональную ссылку, но посмотреть отправленные по ней сообщения сможете только после подписки на канал спонсора: https://t.me/orgasmic_energy   ')
def checkSubChannel(chat_member):
    #print(chat_member.status)
    if chat_member.status!='left':
         return True
    else:
        return False
    
@bot.message_handler(commands=['start'])
def start(message):
    global targetID
    targetID=message.text.split(" ")[-1]
    #print("это id  цели",targetID)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('получить ссылку')
    markup.add(item1)
    if targetID=='/start':
      bot.send_photo(message.chat.id,photo=open('1.jpg','rb'))
      bot.send_photo(message.chat.id,photo=open('2.jpg','rb'))
      bot.send_message(message.chat.id,'Чтобы начать получать анонимные валентинки от своих друзей и знакомых, размести эту ссылку в любой соц.сети: https://t.me/Anonymess_bot?start='+str(message.chat.id)+' \n Важное примечание! Вы можете получить свою персональную ссылку, но посмотреть отправленные по ней сообщения сможете только после подписки на канал спонсора: https://t.me/orgasmic_energy ')
    else:
      mesFromBot=bot.send_message(message.chat.id,'Напишите своё анонимное признание этому человеку')
      bot.register_next_step_handler(mesFromBot,sendMessage)
      
def sendMessage(message):
  #print(message)
  if message.text!=None:
    if checkSubChannel(bot.get_chat_member(chat_id='@orgasmic_energy',user_id=int(targetID))):
      bot.send_message(targetID,'Вам пришло анонимное сообщение:'+message.text+'')
      bot.send_message(message.chat.id,"Ваше сообщение отправлено")
    else:
      bot.send_message(targetID,'подпишись на канал спонсора( https://t.me/orgasmic_energy) чтобы увидеть сообщение')#targetIDmessage.chat.id
      bot.send_message(message.chat.id,"Ваше сообщение отправлено")  
  else:
    bot.send_message(message.chat.id,"Пока что бот может отправлять только текстовые сообщения")

    
@bot.message_handler(content_types=['text'])
def checkRequest(message):    
    if message.text=='получить ссылку':
       getLink(message)
    else:
       bot.send_message(message.chat.id,"Бот не знает такой команды")
bot.polling(none_stop=True)
