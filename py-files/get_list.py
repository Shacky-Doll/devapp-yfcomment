#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

import sys
sys.path.append("/Users/shakuto/Python/Webスクレイピング/yahooファイナンス掲示板スクレイピング/py-files")
from get_info import get_info
#from get_meta import get_meta

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