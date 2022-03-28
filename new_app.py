from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

import streamlit as st

import pandas as pd
import re
import time

from datetime import datetime


scroll_wait_time = 1




def extract_date(string):
    date_pattern = re.compile("(\d{4})/(\d{1,2})/(\d{1,2})")
    
    result = date_pattern.search(string)
   
    y, m, d = result.groups()
    
    if result:
        return str(y) + str(m.zfill(2)) + str(d.zfill(2))
    else:
        return None


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


def get_text_by_elem(elem):
    try:
        text = elem.text
        text = text.replace("\n", "  ")
        text = text.strip()
        return text
    except Exception as e:
        return None


def get_info(comment_id, data):
    soup = BeautifulSoup(data, features = "lxml")
    
    try:    
        comNum = get_text_by_elem(soup.find(class_ = "comNum"))
        comNum = re.sub("\D", "", comNum)

        user_elem = soup.find(class_ = "comWriter")
        user_elem = user_elem.find("a")

        user_id = user_elem["data-user"]

        user_name = get_text_by_elem(user_elem)

        emotion = ""
        emotion_elem = soup.find(class_ = "comWriter").find(class_ = "emotionLabel")

        if emotion_elem:
            emotion = get_text_by_elem(emotion_elem)

        datetime_elem = soup.find(class_ = "comWriter").find_all("span")[-1]

        datetime = get_text_by_elem(datetime_elem)

        comment_reply_target = 0
        comment_reply_dsp = ""
        comment_reply_elem = soup.find(class_ = "comReplyTo")

        if comment_reply_elem:
            comment_reply_target = comment_reply_elem.find("a")["data-parent_comment"]
            comment_reply_dsp = get_text_by_elem(comment_reply_elem)

        comment_text = get_text_by_elem(soup.find(class_ = "comText"))

        info = {}
        info["comment_id"] = comment_id
        info["comment_number"] = comNum
        info["user_id"] = user_id
        info["user_name"] = user_name
        info["emotion"] = emotion
        info["datetime"] = datetime
        info["comment_reply_target"] = comment_reply_target
        info["comment_reply_dsp"] = comment_reply_dsp
        info["comment_text"] = comment_text

        return info
    except Exception as e:
        return None

def get_list(driver, meta_info):
    list = []
    
    elems = driver.find_elements_by_class_name("comment")

    for elem in elems:
        tag = elem.get_attribute("innerHTML")
        comment_id = elem.get_attribute("data-comment")
        info = get_info(comment_id, tag)

        try:
            info.update(meta_info)
            list.append(info)
        except Exception as e:
            None
            
    return list


def scroll_to_elem(driver):
    elems = driver.find_elements_by_class_name("comment")

    last_elem = elems[-1]

    com_number = last_elem.find_element_by_class_name("comNum").text
    com_number = int(com_number)

    actions = ActionChains(driver)
    actions.move_to_element(last_elem)
    actions.perform()
    
    return com_number


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


def add_year(list):
    this_year = f"{str(datetime.now().year)}年"

    date_list = [this_year + value if len(value) <= 12 else value for value in list]
    return date_list


def get_df_comment(url):
    comment_list = get_comment(url)
    
    df = pd.DataFrame(comment_list)
    df = df[["comment_id", "user_name", "datetime", "comment_text"]]
    df["datetime"] = add_year(df["datetime"])
    df["datetime"] = pd.to_datetime(df["datetime"], format = "%Y年%m月%d日 %H:%M")
    df.set_index("comment_id", inplace = True)

    return df


def get_url(text):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options = options, executable_path = '/Users/shakuto/opt/anaconda3/lib/python3.8/site-packages/chromedriver_binary/chromedriver')
    driver.get("https://finance.yahoo.co.jp/")

    elem_input = driver.find_element_by_xpath("/html/body/div/div[3]/header/div/div/div/form/input")
    elem_input.send_keys(text)

    elem_click = driver.find_element_by_xpath("/html/body/div/div[3]/header/div/div/div/form/button/span[2]")
    elem_click.click()

    elem_pribbs = driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[1]/div[3]/ul/li[6]")
    elem_pribbs.click()

    cur_url = driver.current_url
    return cur_url

@st.cache
def get_comment_from_text(text):
    url = get_url(text)

    df = get_df_comment(url)
    
    return(df)




st.title("ヤフーファイナンス掲示板コメント抽出アプリ")

text = st.text_input("銘柄コード、ティッカーコードを入力してください。")
f"{text}の掲示板のコメントを表示します。"

if not text:
    st.error("上の空欄に銘柄コードかティッカーコードを入力してください。")
else:
    df = get_comment_from_text(f"{text}")

    st.subheader(f"{text}の掲示板コメント")
    st.dataframe(df)