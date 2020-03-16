import requests
from bs4 import BeautifulSoup
import csv


def auth(url):
    authUrl = 'https://support.mfisoft.ru/staff/index.php?/Core/Default/Login'
    session = requests.Session()
    data = {"username": 'd.seldev@RTK-IT.ru',
            "password": 'C5Sj3z6TR',
            "submitbutton": "Login",
            "remember": '0',
            "languagecode": "en-us",
            "_ca": "login",
            "_redirectAction": ''
            }
    r = session.post(authUrl, data)
    r2 = session.get(url)
    return r2.text


def get_table_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='gridlayoutborder').find(
        'tbody', class_='gridcontents_ticketmanagegrid_parent').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        ticketID = tds[5].find('a').text
        subject = tds[6].find('a').text
        owner = tds[7].text
        priority = tds[8].text
        status = tds[9].text
        lastActivity = tds[10].text
        ticketUrl = tds[5].find('a').get('href')
        RnD = get_rnd(auth(ticketUrl))
        comment = get_comment(auth(ticketUrl))

        data = {'ticketID': ticketID,
                'subject': subject,
                'owner': owner,
                'priority': priority,
                'status': status,
                'lastActivity': lastActivity,
                'RnD': RnD,
                'comment': comment,
                'ticketUrl': ticketUrl}
        write_csv(data)


def get_rnd(url):
    soup = BeautifulSoup(url, 'lxml')
    try:
        rnd = soup.find_all('div', class_ = 'customfieldstaticcontent')[2].find_all('td', class_='customfieldcol2_pink')[4].text
    except IndexError:
        rnd = 'null'
    return rnd


def get_comment(url):
    soup = BeautifulSoup(url, 'lxml')
    try:
        comment = soup.find_all('div', class_ = 'customfieldstaticcontent')[2].find_all('td', class_='customfieldcol2_pink')[3].text
    except IndexError:
        comment = 'null'
    return comment
    # try:
    #     comment = soup.find('div', id='ticketnotescontainerdiv').find_all('p')[-1].text
    # except IndexError:
    #     comment = 'null'
    # return comment


def write_csv(data):
    with open('kayako.csv', 'a', encoding='cp1251') as f:
        writer = csv.writer(f, delimiter='^')

# def write_csv(data):
#     with open('kayako.csv', 'a', newline='', encoding='cp1251') as f:
#         writer = csv.writer(f,delimiter='^',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(
            [data['ticketID'],
             data['subject'],
             data['owner'],
             data['priority'],
             data['status'],
             data['lastActivity'],
             data['RnD'],
             data['comment'],
             data['ticketUrl']]
        )


def get_authUser():
    mainPage = 'https://support.mfisoft.ru/staff/index.php?/Base/Home/Index'
    soup = BeautifulSoup(mainPage, 'lxml')
    authUser = soup.find('div', class_='dashboardusername').text
    return authUser


def main():
    allTickets = 'https://support.mfisoft.ru/staff/index.php?/Tickets/Manage/Index'
    resolvedTicket = 'https://support.mfisoft.ru/staff/index.php?/Tickets/Manage/Filter/31/6/-1'
    get_table_data(auth(allTickets))
    get_table_data(auth(resolvedTicket))

if __name__ == "__main__":
    main()
