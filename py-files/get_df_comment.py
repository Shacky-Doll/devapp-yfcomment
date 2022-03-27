import pandas as pd, sys
pd.set_option('display.width', 1000)

sys.path.append("/Users/shakuto/Python/Webスクレイピング/yahooファイナンス掲示板スクレイピング/py-files")
from get_comment import get_comment
from add_year import add_year

def get_df_comment(url):
    comment_list = get_comment(url)
    
    df = pd.DataFrame(comment_list)
    df = df[["comment_id", "user_name", "datetime", "comment_text"]]
    df["datetime"] = add_year(df["datetime"])
    df["datetime"] = pd.to_datetime(df["datetime"], format = "%Y年%m月%d日 %H:%M")
    df.set_index("comment_id", inplace = True)

    return df