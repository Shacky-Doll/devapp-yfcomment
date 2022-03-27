from selenium import webdriver

def get_text_by_elem(elem):
    try:
        text = elem.text
        text = text.replace("\n", "  ")
        text = text.strip()
        return text
    except Exception as e:
        return None