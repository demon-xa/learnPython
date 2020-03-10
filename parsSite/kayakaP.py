import requests

def loginbot(login,password):
    s = requests.session()
    s.get("https://support.mfisoft.ru/staff/")
    data = {"username": 'login',
            "password": 'password',
            "submitbutton": "Login",
            "remember": '0',
            "languagecode": "en-us",
            "_ca": "login",
            "_redirectAction": ''
    }

    r = s.post("https://support.mfisoft.ru/staff/index.php?/Core/Default/Login", data=data)
