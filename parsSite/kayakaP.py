import requests
from bs4 import BeautefulSoup
import csv



def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def write_csv(data):
    with open('cms.cvs', 'a') as f:
        writer = csv.writer(f)
        pass

def get_page_data(html):
    soup = BeautefulSoup(html, 'lxml')

def main()
    pass


def if __name__ == "__main__":
    main()