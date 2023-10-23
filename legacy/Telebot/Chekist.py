
import requests
import json
import time

def json2arr(jsonObj):
      return json.loads(jsonObj.content)
def mentions(userId):
  ref="https://vk.com/feed?obj="+str(userId)+"&q=&section=mentions"
  return ref
def hideFriends(userId,token):
  arrPhotos=[]
  arrLikes=[]
  arrHideFriends=[]
  photosParams=requests.get("https://api.vk.com/method/photos.get?rev=1&owner_id="+str(userId)+"&count=10&access_token="+token+"&album_id=profile&v=5.126")
  photosParams=json2arr(photosParams)["response"]["items"]
  for item in photosParams:
    photo=item['id']
    time.sleep(1)
    arrPhotos.append(photo)
    print(arrPhotos)
  time.sleep(1)
  for item in arrPhotos:
     photoLiked=item    
     time.sleep(1)
     Likes=requests.get("https://api.vk.com/method/likes.getList?owner_id="+str(userId)+"&item_id="+str(photoLiked)+"&type=photo&access_token="+token+"&v=5.126")
     Likes=json2arr(Likes)
     Likes=Likes['response']['items']
     arrLikes=arrLikes+Likes
  arrLikes=list(set(arrLikes))
  UserFriends=requests.get("https://api.vk.com/method/friends.get?user_id="+str(userId)+"&access_token="+token+"&v=5.126")
  UserFriends=json2arr(UserFriends)
  UserFriends=UserFriends['response']['items']
  setHonest=set(arrLikes).intersection(set(UserFriends))
  setSuspects=set(arrLikes)-setHonest
  arrSuspects=list(setSuspects)
  for item in arrSuspects:
        id=item
        suspectFriends=requests.get("https://api.vk.com/method/friends.get?user_id="+str(id)+"&access_token="+token+"&v=5.126")
        suspectFriends=json2arr(suspectFriends)
        if not ( "response" in suspectFriends):
             print("not hasattr id=",id)
             continue
        suspectFriends=suspectFriends['response']['items']        
        if userId in suspectFriends:
          arrHideFriends.append(id)
          print("есть контакт",id)
        else:
          pass
        time.sleep(0.5)
  print('кончился вальс')
  print("кртые друзья:",arrHideFriends)
  arrHideFriendsLinks=[]
  for item in arrHideFriends:
        friendId=item
        print(friendId)
        link="https://vk.com/id"+str(friendId)+""
        arrHideFriendsLinks.append(link)
  return arrHideFriends
def getUserInfo(userId,token,res):
  userInfo=requests.get("https://api.vk.com/method/users.get?user_ids="+str(userId)+"&access_token="+token+"&v=5.126")
  userInfo=json2arr(userInfo)
  userInfo=userInfo["response"]
  userInfo=userInfo[0]
  name=userInfo["first_name"]
  surname=userInfo["last_name"]
#  userInfo="Имя:"+name+",Фамилия:"+surname+",Id:"+str(userId)+""
  userInfo = {}
  hiddenFriends =[]
  userInfo["name"] = name
  userInfo["surname"] = surname
  userInfo["userId"] = userId
  userInfo["mentions"]= mentions(userId)
  for item in res :
    hf = {}
    hfInfo=requests.get("https://api.vk.com/method/users.get?user_ids="+str(item)+"&access_token="+token+"&v=5.126")
    hfInfo=json2arr(hfInfo)
    print(hfInfo)
    hfInfo=hfInfo["response"]
    hfInfo=hfInfo[0]
    hf["name"] =hfInfo["first_name"]
    hf["surname"] =hfInfo["last_name"]
    hf["link"] ="https://vk.com/id"+str(item)+""
    hiddenFriends.append(hf)
  userInfo["hiddenFriends"] = hiddenFriends 
  return userInfo
def searchHiddenFriendsAndMentions(paramsDict):
  token = paramsDict.setdefault("token", "Не задано")
  userId = int(paramsDict.setdefault("userId", 0))  
  res=hideFriends(userId,token)
  userinfo=getUserInfo(userId,token,res)
  return userinfo

