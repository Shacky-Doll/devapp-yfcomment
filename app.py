import streamlit as st
import os, sys

sys.path.append('/Users/shakuto/Python/Webスクレイピング/yahooファイナンス掲示板スクレイピング/py-files')
from get_url import get_url
from get_df_comment import get_df_comment


st.title("ヤフーファイナンス掲示板コメント抽出アプリ")

text = st.text_input("銘柄コード、ティッカーコードを入力してください。")
f"{text}の掲示板のコメントを表示します。"

@st.cache
def get_comment_from_text(text):
    url = get_url(text)

    df = get_df_comment(url)
    
    return(df)


if not text:
    st.error("上の空欄に銘柄コードかティッカーコードを入力してください。")
else:
    df = get_comment_from_text(f"{text}")

    st.subheader(f"{text}の掲示板コメント　　　　　　")
    st.dataframe(df)