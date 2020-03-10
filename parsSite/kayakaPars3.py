import requests
from bs4 import BeautifulSoup

class kayaka(object):

    def auth(self):
        url = 'https://support.mfisoft.ru/staff/index.php?/Core/Default/Login'
        session = requests.Session()
        data = {"username": 'd.seldev@RTK-IT.ru',
                "password": 'C5Sj3z6TR',
                "submitbutton": "Login",
                "remember": '0',
                "languagecode": "en-us",
                "_ca": "login",
                "_redirectAction": ''
                }
        r = session.post(url, data)
#        print(r.text)
        url2 = 'https://support.mfisoft.ru/staff/index.php?/Base/Home/Index'
        g = session.get(url2)
        print(g.text)

 
if __name__ == "__main__":
    Kayaka = kayaka()
    Kayaka.auth()