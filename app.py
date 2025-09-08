import streamlit as st

st.title("Hello, Streamlit!")
st.write("これは最小構成の Streamlit アプリです。")

# ユーザーに数字を入力させる
a = st.number_input("1つ目の数字を入力してください", value=0)
b = st.number_input("2つ目の数字を入力してください", value=0)

# ボタンを押すと答えを表示
st.write("##### 計算結果")
st.write(f"{a} ✖️ {b} = {a * b}")