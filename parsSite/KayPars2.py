import requests

def login(username, password):
    session = requests.Session()
    data = {"username":"username", "password":"password"}
    url = "https://support.mfisoft.ru/staff/index.php?/Core/Default/Login"
    data = {"username": 'login',
            "password": 'password',
            "submitbutton": "Login",
            "remember": '0',
            "languagecode": "en-us",
            "_ca": "login",
            "_redirectAction": ''
    }
    response = session.post(url, data=data)
