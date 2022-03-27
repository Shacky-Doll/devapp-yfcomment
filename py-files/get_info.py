from bs4 import BeautifulSoup
import re, os, sys
sys.path.append('/Users/shakuto/Python/Webスクレイピング/yahooファイナンス掲示板スクレイピング/py-files')
from get_text_by_elem import get_text_by_elem


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