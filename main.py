import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_phone_numbers(website: str, hard_search:bool=False, by_links:bool=True) -> list[str]:
    content = parse_website(website, hard_search)

    if by_links:
        phone_numbers = []
        soup = BeautifulSoup(content, 'html.parser')
        #if website == 'https://hands.ru/company/about/':
            #print(soup.prettify())
        for phone in soup.select('a[href^="tel:"]'):
            clean_phone = phone.get('href').replace('tel:', '')
            if clean_phone not in phone_numbers:
                phone_numbers.append(clean_phone)
    else:
        r = re.compile(r'(\+7|8)[- _]*\(?[- _]*(\d{3}[- _]*\)?([- _]*\d){7}|\d\d[- _]*\d\d[- _]*\)?([- _]*\d){6})')
        phone_numbers = [p.group() for p in r.finditer(content)]

    return phone_numbers


def parse_website(website: str, hard_search: bool=False) -> str:
    if not hard_search:
        response = requests.get(website)
        content = response.text

    else:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.set_preference("dom.disable_beforeunload", True)
        driver = webdriver.Firefox(options=options)
        driver.get(website)
        reveal_hidden_number(driver, ['phone'])
        content = driver.page_source
        driver.quit()

    return content


def reveal_hidden_number(driver: webdriver.Firefox, key_words: list[str], timeout: float=0.5) -> None:
    time.sleep(timeout)
    for key_word in key_words:
        for element in driver.find_elements(By.XPATH, f'//button[contains(@class, "{key_word}")]'):
            element.click()


websites = ['https://profi.ru/',
            'https://hands.ru/',
            'https://hands.ru/company/about/',
            'https://repetitors.info/',
            'https://mipt.ru/']

for website in websites:
    print(f'Page {website}, phones: {get_phone_numbers(website=website, hard_search=True)}')
