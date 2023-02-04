import re
import requests
from headers import get_headers

def get_html(url):
    response = requests.get(url, headers=get_headers(), verify=True)
    return response.text

def get_pages(url):
    i = 1
    pages = []
    while True:
        html = get_html(f"{url}/page/{i}")
        if "You blew up the Internet." in html:
            break
        pages.append(html)
        i += 1
    return pages

if __name__ == "__main__":
    pages = get_pages("https://iriedirect.com/irie-direct")
    for page in pages:
        print(len(page))
