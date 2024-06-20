# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from time import sleep
import re

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
    def createDataFrame(self):
        items_list = self.browser.find_elements(By.XPATH, value="//table/tbody/tr[contains(@itemtype, 'http://schema.org/Book')]")
        img = self.browser.find_elements(By.CLASS_NAME, value="bookCover")
        book_list = list()
        for i in range(len(items_list)):
            book_list.append(items_list[i].text.split('\n'))
        book_list_ap = [{} for _ in range(len(book_list))]

        for i in range(0,len(book_list)):
            # use this to fetch avg rating, total ratings and published date -> book_list[i][2]
            rating_string = book_list[i][2]

            avg_rating_match = re.search(r"(\d+\.\d+) avg rating",rating_string)
            total_ratings_match = re.search(r"(\d{1,3}(?:,\d{3})*) ratings", rating_string)
            published_date_match = re.search(r"published (\d{4})", rating_string)

            avg_rating = avg_rating_match.group(1) if avg_rating_match else None
            total_ratings = total_ratings_match.group(1) if total_ratings_match else None
            published_date = published_date_match.group(1) if published_date_match else None


            book_list_ap[i] = {'title':book_list[i][0],
                                'author':book_list[i][1],
                                'published_date': published_date,
                                'avg_rating':avg_rating,
                                'total_ratings':total_ratings,
                                'cover_img': img[i].get_property("src") 
            }
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
    def link_to_open(self, link):
        self.browser.get(link)
        eof = True
        while eof:
            try:
                must_read = self.browser.find_element(By.XPATH, value="//a[contains(text(), 'Must Read')]")
                if must_read:
                    eof = False
            except:
                next_page = self.browser.find_element(By.XPATH, value="//a[contains(@class, 'next_page')]")
                next_page.click()

        self.browser.get(must_read.get_property("href"))
        return self.createDataFrame()
    # End of open link_to_open
    # ################################################


    # ################################################
    # Search Module
    def searchModule(self,book_name):
        self.browser.get('https://www.goodreads.com/search?q=&qid=')
        search_book = self.browser.find_element(By.ID, value="search_query_main")
        search_book.send_keys(book_name)
        search_book.submit()
        return self.createDataFrame()
    # Search Module Ends
    # ################################################

