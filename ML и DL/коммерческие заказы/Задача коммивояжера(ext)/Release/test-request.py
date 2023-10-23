import requests
response=requests.post('http://127.0.0.1:8000/items', json={"listcity":["Калуга","Сортавала","Санкт-Петербург","Москва"]})
print(response.text)
