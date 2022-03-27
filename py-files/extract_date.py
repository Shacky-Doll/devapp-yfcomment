import re

def extract_date(string):
    date_pattern = re.compile("(\d{4})/(\d{1,2})/(\d{1,2})")
    
    result = date_pattern.search(string)
   
    y, m, d = result.groups()
    
    if result:
        return str(y) + str(m.zfill(2)) + str(d.zfill(2))
    else:
        return None