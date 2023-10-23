import requests
response=requests.post('http://127.0.0.1:8000/mail',json={"mail":"sevasubbotin@yandex.ru","photo":"18.jpg"})
print(response.content)
