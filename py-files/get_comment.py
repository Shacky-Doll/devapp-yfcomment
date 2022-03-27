from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

import os, sys
sys.path.append('/Users/shakuto/Python/Webスクレイピング/yahooファイナンス掲示板スクレイピング/py-files')
from get_meta import get_meta
from scroll_to_elem import  scroll_to_elem
from get_list import get_list

scroll_wait_time = 1

def get_comment(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options = options)
    driver.get(url)
    driver.implicitly_wait(10)

    meta_info = get_meta(driver)

    last_com_number = 99999

    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    while last_com_number > 1:
        com_number = scroll_to_elem(driver)
        time.sleep(scroll_wait_time)

        if com_number == last_com_number:
            break
        else:
            last_com_number = com_number

    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    comment_list = get_list(driver, meta_info)

    driver.quit()

    return comment_list