import os, sys
sys.path.append('/Users/shakuto/Python/Webスクレイピング/yahooファイナンス掲示板スクレイピング/py-files')
from get_url import get_url
from get_df_comment import get_df_comment

def get_comment_from_text(text):
    url = get_url(text)

    df = get_df_comment(url)
    
    return(df)