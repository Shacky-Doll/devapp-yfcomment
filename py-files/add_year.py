from datetime import datetime

def add_year(list):
    this_year = f"{str(datetime.now().year)}年"

    date_list = [this_year + value if len(value) <= 12 else value for value in list]
    return date_list