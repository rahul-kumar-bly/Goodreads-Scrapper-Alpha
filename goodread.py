# import libraries
from tkinter import BROWSE
from tkinter.messagebox import RETRY
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# import libraries end
# ################################################
class GoodreadAPI():
    # ################################################
    # pre-requiste
    def __init__(self, email, password):
        self.email = email
        self.password = password
    s = Service("chromedriver.exe")
    opts = Options()
    opts.headless = True
    browser = webdriver.Chrome(options=opts,service=s)
    # browser = webdriver.Chrome(service=s)
    browser.get('https://www.goodreads.com/user/sign_in')
    # ################################################

        # ################################################
        # Login Information
    def login(self):
        log_email = self.browser.find_element(By.ID, value="user_email")
        log_pwd = self.browser.find_element(By.ID, value="user_password")
        log_email.send_keys(self.email)
        log_pwd.send_keys(self.password)
        log_pwd.submit()
        # Login Information end
        # ################################################


    # ################################################
    # This will create dataframe (tuple)
    def createDataFrame(self,source):
        itemqueue = self.browser.find_elements(By.XPATH, value="//table/tbody/tr[contains(@itemtype, 'http://schema.org/Book')]")
        img = self.browser.find_elements(By.CLASS_NAME, value="bookCover")
        book_list = list()
        for i in range(len(itemqueue)):
            book_list.append(itemqueue[i].text.split('\n'))
        book_list_ap = list()
        if source == "list":
            for i in range(0,len(book_list)):
                book_list_ap.append((book_list[i][1],book_list[i][2],book_list[i][3],img[i].get_property("src")))
        elif source == "search":
            for i in range(0,len(book_list)):
                book_list_ap.append((book_list[i][0],book_list[i][1],book_list[i][2],img[i].get_property("src")))
        return book_list_ap
    # This will create dataframe (tuple) Ends
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
        return self.createDataFrame(source="list")
    # End of open link_to_open
    # ################################################


    # ################################################
    # Search Module
    def searchModule(self,book_name):
        self.browser.get('https://www.goodreads.com/search?q=&qid=')
        search_book = self.browser.find_element(By.ID, value="search_query_main")
        search_book.send_keys(book_name)
        search_book.submit()
        return self.createDataFrame(source="search")
    # Search Module Ends
    # ################################################

