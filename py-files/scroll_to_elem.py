#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def scroll_to_elem(driver):
    elems = driver.find_elements_by_class_name("comment")

    last_elem = elems[-1]

    com_number = last_elem.find_element_by_class_name("comNum").text
    com_number = int(com_number)

    actions = ActionChains(driver)
    actions.move_to_element(last_elem)
    actions.perform()
    
    return com_number