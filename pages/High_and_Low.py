import streamlit as st
import random

st.title("High and Low Game!")

st.write("数字を予想して、High か Low かを当ててください。")

# トランプは 1～13（A=1, J=11, Q=12, K=13）にして簡略化
if "current_card" not in st.session_state:
    st.session_state.current_card = random.randint(1, 13)

st.write(f"現在のカード: **{st.session_state.current_card}**")

# ボタンを押すと次のカードを引く
if st.button("High"):
    next_card = random.randint(1, 13)
    st.write(f"次のカード: **{next_card}**")
    if next_card > st.session_state.current_card:
        st.success("You Win! 🎉")
    elif next_card < st.session_state.current_card:
        st.error("You Lose 💔")
    else:
        st.info("Draw 🤝")
    st.session_state.current_card = next_card

if st.button("Low"):
    next_card = random.randint(1, 13)
    st.write(f"次のカード: **{next_card}**")
    if next_card < st.session_state.current_card:
        st.success("You Win! 🎉")
    elif next_card > st.session_state.current_card:
        st.error("You Lose 💔")
    else:
        st.info("Draw 🤝")
    st.session_state.current_card = next_card

