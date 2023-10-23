import logging
import requests
import json
import time
def searchFriends(token,userId,cityGroup1,cityGroup2,cityGroup3,hobbyGroup1,hobbyGroup2,hobbyGroup3):

  dashaId=userId
  offset=0
  arrCityMembers1=[]
  arrCityMembers2=[]
  arrCityMembers3=[]
  arrCultMembers1=[]
  arrCultMembers2=[]
  arrCultMembers3=[]
  count=0
  def json2arr(jsonObj):
      return json.loads(jsonObj.content)

  def getMembersBy(groupID):
    return requests.get("https://api.vk.com/method/groups.getMembers?group_id="+groupID+"&offset="+str(offset)+"&access_token="+token+"&v=5.126")

  def getArrMembers(groupID):
    res=[]
    if groupID=='':
      return res
    offset=0
    offsetIsDown = False;
    maxTryCount = 2
    tryCount = 1
    while True:
#     groupID=hobbyGroup1
      users=json2arr(getMembersBy(groupID))
      if not ("response" in users):
        logging.debug("Нет ответа от сервера VK. Попытка " + str(tryCount))
        if offsetIsDown:
          pass
        else:
          offset=offset-1000
          offsetIsDown = True
#        time.sleep(12000)
        time.sleep(3)
        tryCount = tryCount + 1
        if tryCount >= maxTryCount:
          break 
        continue
      offsetIsDown = False
      count=users["response"]["count"]
      if offset>count:
        break
      offset=offset+1000
      usersItem=users["response"]["items"]
#      arrCultMembers1=usersItem+arrCultMembers1
      res=usersItem+res
#      print(len(arrCultMembers1),groupID)
      logging.debug(len(res),groupID)
      time.sleep(1)      
    offset=0
    return res
  arrCityMembers1=getArrMembers(cityGroup1)   
  arrCityMembers2=getArrMembers(cityGroup2)
  arrCityMembers3=getArrMembers(cityGroup3) 
  arrCultMembers1=getArrMembers(hobbyGroup1)   
  arrCultMembers2=getArrMembers(hobbyGroup2)   
  arrCultMembers3=getArrMembers(hobbyGroup3)   


#----массивы городов и интересов
  setCity=set(arrCityMembers1+arrCityMembers3+arrCityMembers2)
  setCult=set(arrCultMembers1+arrCultMembers2+arrCultMembers3)
#----массив потенциальных друзей
  arrSuspects=list(setCity.intersection(setCult))
  logging.debug(arrSuspects)
  def getFriendsById(id):
    return requests.get("https://api.vk.com/method/friends.get?user_id="+str(id)+"&access_token="+token+"&v=5.126")
  arrContact=[]
  for id in arrSuspects:
    arrJsonFriends=getFriendsById(id)
    logging.debug("arrJsonFriends=",arrJsonFriends)
    arrFriends=json.loads(arrJsonFriends.content)
    logging.debug("arrFriends=",arrFriends)
    if not ( "response" in arrFriends):
      logging.debug("not hasattr id=",id)
      continue
    arrFriends=list(arrFriends["response"]["items"])
    logging.debug("id=",id)
    if dashaId in arrFriends:
      arrContact.append(id)
      logging.debug("есть контакт",id)
    else:
      pass
    time.sleep(90)
  logging.debug(arrContact)
  return arrContact
"""
token="6b8e437ffaa729cc3038ff59bc34b0c9dbf2f279cde5f63067c362bada49b2cf0b2562e1f0ab088937118"
userId=278490559
cityGroup1="aircraft_gallery_group"
cityGroup2="201181792"
cityGroup3="201181792"
hobbyGroup1="nuclearinc2"
hobbyGroup2="201181792"
hobbyGroup3="201181792"
searchFriends(token,userId,cityGroup1,cityGroup2,cityGroup3,hobbyGroup1,hobbyGroup2,hobbyGroup3)
"""

    
    
