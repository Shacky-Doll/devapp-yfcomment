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

extract_date('うざいね。3月26日 11:22')