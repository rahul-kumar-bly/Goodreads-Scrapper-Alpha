# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from time import sleep
import re
import requests
from bs4 import BeautifulSoup

# import libraries end
# ################################################
class GoodreadAPI():
    # ################################################
    # pre-requiste
    def __init__(self, email, password):
        self.email = email
        self.password = password
    options = uc.ChromeOptions()
    # options.add_argument("--headless")
    browser = uc.Chrome(options=options)
    browser.get('https://www.goodreads.com/user/sign_in')
    # ################################################

        # ################################################
        # Login Information
    def login(self):
        login_with_email_button = self.browser.find_element(By.CSS_SELECTOR, value=".authPortalConnectButton.authPortalSignInButton")
        login_with_email_button.click()
        sleep(2)
        log_email = self.browser.find_element(By.ID, value="ap_email")
        log_pwd = self.browser.find_element(By.ID, value="ap_password")
        log_email.send_keys(self.email)
        log_pwd.send_keys(self.password)
        log_pwd.submit()
        # Login Information end
        # ################################################


    # ################################################
    # This will create dataframe (tuple)
    def createDataFrame(self, search_response):
        soup = BeautifulSoup(search_response, 'html.parser')
        items_list = soup.find_all('tr', {'itemtype': 'http://schema.org/Book'})
        print(f"length of items_list is {len(items_list)}")
        book_list_ap = [{} for _ in range(len(items_list))]

        for i in range(0,len(items_list)):
            # use this to fetch avg rating, total ratings and published date -> book_list[i][2]
            rating_string = items_list[i].find('span', {'class', 'greyText smallText uitext'}).text.strip().replace('\n', '')
            print(f'rating_string is {rating_string}')
            avg_rating_match = re.search(r"(\d+\.\d+) avg rating",rating_string)
            total_ratings_match = re.search(r"(\d{1,3}(?:,\d{3})*) ratings", rating_string)
            published_date_match = re.search(r"published\s+(\d{4})", rating_string)

            avg_rating = avg_rating_match.group(1) if avg_rating_match else None
            print(f'avg_rating is {avg_rating}')
            total_ratings = total_ratings_match.group(1) if total_ratings_match else None
            published_date = published_date_match.group(1) if published_date_match else None

            book_list_ap[i] = {
                'title': items_list[i].find('a', title=True)['title'],
                'author': items_list[i].find('a', {'class': 'authorName'}).text.strip(),
                'published_date': published_date,
                'avg_rating':avg_rating,
                'total_ratings':total_ratings,
                'cover_img': items_list[i].find('img', {'class': 'bookCover'})['src']
            }

        print(book_list_ap)
        return book_list_ap
    # This will create dataframe Ends
    # ################################################


    # ################################################
    # This will create a list of tags
    def tags_list(self):
        self.browser.get("https://www.goodreads.com/list")
        tag_text = self.browser.find_elements(By.XPATH, value="//ul[contains(@class, 'listTagsTwoColumn')]/li/a")
        tag_row = self.browser.find_elements(By.XPATH, value="//ul[contains(@class, 'listTagsTwoColumn')]/li/a")
        tag_list = list()
        for i in tag_row:
            tag_list.append(i.get_property("href"))
        return tag_list
    # End of tags_list
    # ################################################

    # ################################################
    # This will open tag list
    # def link_to_open(self, link):
    #     self.browser.get(link)
    #     eof = True
    #     while eof:
    #         try:
    #             must_read = self.browser.find_element(By.XPATH, value="//a[contains(text(), 'Must Read')]")
    #             if must_read:
    #                 eof = False
    #         except:
    #             next_page = self.browser.find_element(By.XPATH, value="//a[contains(@class, 'next_page')]")
    #             next_page.click()

    #     self.browser.get(must_read.get_property("href"))
    #     return self.createDataFrame(self, "")
    # End of open link_to_open
    # ################################################


    # ################################################
    # Search Module
    def searchModule(self,search_q):
        query = "+".join(search_q.strip().split())
        search_url = f"https://www.goodreads.com/search?q={query}&qid="
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
        response = requests.get(search_url, headers=headers)
        print(f'search_url is {search_url}')
        print(f'response.status_code is {response.status_code}')
        if response.status_code == 200:
            search_response = response.text
            return self.createDataFrame(search_response)
        else:
            return 
    
    # Search Module Ends
    # ################################################

