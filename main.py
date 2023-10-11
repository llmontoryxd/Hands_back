import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver


def get_phone_numbers(website: str, hard_search:bool=False, by_links:bool=True) -> list[str]:
    content = parse_website(website, hard_search)
    if by_links:
        phone_numbers = []
        soup = BeautifulSoup(content, 'html.parser')
        for phone in soup.select('a[href^="tel:"]'):
            clean_phone = phone.get('href').replace('tel:', '')
            if clean_phone not in phone_numbers:
                phone_numbers.append(clean_phone)
    else:
        r = re.compile(r'(\+7|8)[- _]*\(?[- _]*(\d{3}[- _]*\)?([- _]*\d){7}|\d\d[- _]*\d\d[- _]*\)?([- _]*\d){6})')
        phone_numbers = [p.group() for p in r.finditer(content)]

    return phone_numbers


def parse_website(website: str, hard_search:bool=False) -> str:
    if not hard_search:
        response = requests.get(website)
        content = response.text
    else:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get(website)
        content = driver.page_source

    return content


websites = ['https://profi.ru/', 'https://hands.ru/company/about/', 'https://repetitors.info/', 'https://mipt.ru/']
for website in websites:
    print(f'Page {website}, phones: {get_phone_numbers(website=website, hard_search=True)}')