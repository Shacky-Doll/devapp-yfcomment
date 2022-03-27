#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import re, os, sys
sys.path.append('/Users/shakuto/Python/Webスクレイピング/yahooファイナンス掲示板スクレイピング/py-files')
from extract_date import extract_date

def get_meta(driver):
    title = driver.find_element_by_tag_name("h1").text
    try:
        title_list = title.split("-")

        ticker = title_list[0]

        title_list2 = title.split("〜")

        if title_list2[1] == "":
            start_date = extract_date(title_list2[0])
            end_date = ""
        else:
            start_date = extract_date(title_list2[0])
            end_date = extract_date(title_list2[1])
        
        info = {}
        info["Ticker"] = ticker
        info["Start_date"] = start_date
        info["End_date"] = end_date
        return info
    except Exception as e:
        return None