import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
def main():
    pass


if __name__ == "__main__":
    main()

    