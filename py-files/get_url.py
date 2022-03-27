from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_url(text):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options = options)
    driver.get("https://finance.yahoo.co.jp/")

    elem_input = driver.find_element_by_xpath("/html/body/div/div[3]/header/div/div/div/form/input")
    elem_input.send_keys(text)

    elem_click = driver.find_element_by_xpath("/html/body/div/div[3]/header/div/div/div/form/button/span[2]")
    elem_click.click()

    elem_pribbs = driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[1]/div[3]/ul/li[6]")
    elem_pribbs.click()

    cur_url = driver.current_url
    return cur_url