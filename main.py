import goodread
import pandas as pd
from random import randint



# strings literal
WELCOME_STRING = """Please let me know your prefered action.
1.Search a book
2.Show all categories
Your input ===> """
SAVE_FILE = "Save it as CSV file? (y/n) ===> "
DONT_SAVE = "Thanks for using this tool!"
XL_FILE = str(randint(888,9999999)) + ".csv"
SEARCH_STRING = """Enter a book name to search, spelling must be correct. 
===> """
SELECT_A_LINK = "Select a particular link ===> "



goodreader = goodread.GoodreadAPI(email="", password="")
goodreader.login()

# save data
def print_save_df(list_link):
    df = pd.DataFrame(list_link)
    print(df)
    save_to_ = input(SAVE_FILE)
    if save_to_ == "y":
        df.to_csv(XL_FILE)
    else:
        print(DONT_SAVE)


# search
category = int(input(WELCOME_STRING))
if category == 1:
    book_title = input(SEARCH_STRING)
    book_list = goodreader.searchModule(book_title)
    print_save_df(book_list)


# tags
elif category == 2:
    tag_list = goodreader.tags_list()
    df = pd.DataFrame(tag_list)
    print(df)
    selected_tag = int(input(SELECT_A_LINK))
    if selected_tag != " ":
        print("Selected tag is", tag_list[selected_tag])
        tag_link = goodreader.link_to_open(tag_list[selected_tag])
        print_save_df(tag_link)