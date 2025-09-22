# pages/High_and_Low2.py
from model.High_and_Low_model import GameState
import streamlit as st
import pandas as pd

st.set_page_config(page_title="High & Low Mock Player", page_icon="🃏", layout="centered")
st.title("🃏 High & Low モック・ラウンドプレイヤー")




# ==== model生成のみ ====
if "hl_rounds" not in st.session_state:
    st.session_state.hl_rounds = []
if "hl_deck" not in st.session_state:
    st.session_state.hl_deck = [5, 9, 12, 13, 2, 1, 7, 8, 10, 11, 3, 4, 6]
if "hl_chips" not in st.session_state:
    st.session_state.hl_chips = 100
if "hl_idx" not in st.session_state:
    st.session_state.hl_idx = -1

rounds = st.session_state.hl_rounds
deck = st.session_state.hl_deck
init_chips = 100
chips_now = st.session_state.hl_chips
total_rounds = len(rounds)
status = {"game_end": "3 rounds finished" if total_rounds >= 3 else None}

# ==== 進行用のインデックス: -1=開始前, 0..total_rounds-1 = 各ラウンド ====
if "round_idx" not in st.session_state:
    st.session_state.round_idx = -1  # 開始前



# ==== コントロール & ユーザー選択 ====
col_a, col_b, col_c, col_d = st.columns(4)
if col_a.button("⏮️ Reset"):
    st.session_state.hl_rounds = []
    st.session_state.hl_deck = [5, 9, 12, 13, 2, 1, 7, 8, 10, 11, 3, 4, 6]
    st.session_state.hl_chips = 100
    st.session_state.hl_idx = -1
if col_b.button("▶️ Start"):
    st.session_state.hl_idx = 0
    st.session_state.hl_waiting_bet = True
if col_d.button("◀️ Prev", disabled=st.session_state.hl_idx <= -1):
    st.session_state.hl_idx -= 1
idx = st.session_state.hl_idx
if idx == -1 or not rounds:
    chips_now = st.session_state.hl_chips
else:
    chips_now = rounds[idx]["chips_after"]
# ベースカード表示 & ベット入力
if idx >= 0 and ("hl_waiting_bet" in st.session_state and st.session_state.hl_waiting_bet):
    # ベースカードのみ表示
    base_card = st.session_state.hl_deck[0] if idx == 0 and not rounds else rounds[idx]["base_card"]
    st.subheader(f"Round {idx+1}")
    st.markdown(f"<span style='font-size:2em; color:#e74c3c; font-weight:bold;'>ベースカード：{base_card}</span>", unsafe_allow_html=True)
    st.markdown("### ベットと宣言")
    bet = st.number_input("ベット額", min_value=1, max_value=chips_now, value=10, step=1, key="bet_input")
    choice = st.radio("High/Low", ["High", "Low"], horizontal=True, key="choice_input")
    bet_clicked = st.button("Bet")
    if bet_clicked:
        # 新ラウンド生成
        if idx == 0 and not rounds:
            base_deck = st.session_state.hl_deck.copy()
            game = GameState(initial_chips=100, deck=base_deck)
            rr = game.play_round(choice, bet)
            st.session_state.hl_rounds = [rr.__dict__]
            st.session_state.hl_deck = rr.remaining_deck
            st.session_state.hl_chips = rr.chips_after
            st.session_state.hl_idx = 0
        else:
            deck_now = rounds[idx]["remaining_deck"]
            chips_now = rounds[idx]["chips_after"]
            game = GameState(initial_chips=chips_now, deck=deck_now)
            game.round_count = len(rounds)
            game.chips = chips_now
            for r in rounds:
                game.rounds.append(r)
            try:
                rr = game.play_round(choice, bet)
                st.session_state.hl_rounds.append(rr.__dict__)
                st.session_state.hl_deck = rr.remaining_deck
                st.session_state.hl_chips = rr.chips_after
                st.session_state.hl_idx += 1
            except Exception as e:
                st.error(f"ラウンド生成エラー: {e}")
        # 次ラウンドが可能ならベースカード入力状態に遷移
        if len(st.session_state.hl_deck) >= 2 and st.session_state.hl_chips > 0:
            st.session_state.hl_waiting_bet = True
        else:
            st.session_state.hl_waiting_bet = False
# 結果表示
elif idx >= 0 and rounds:
    if 0 <= idx < len(rounds):
        r = rounds[idx]
        st.subheader(f"Round {r['round']}")
        st.markdown(f"<span style='font-size:2em; color:#e74c3c; font-weight:bold;'>ベースカード：{r['base_card']}</span>", unsafe_allow_html=True)
        st.markdown(f"- プレイヤー宣言：**{r['player_choice']}**")
        st.markdown(f"- 結果カード：**{r['result_card']}**")
        st.markdown(f"- 勝敗：**{r['outcome']}**")
        st.markdown(f"- ベット：**{r['bet']}**")
        st.markdown(f"- ラウンド後チップ：**{r['chips_after']}**")
# 任意ジャンプ
jump_min = -1
jump_max = len(st.session_state.hl_rounds) - 1
if jump_min < jump_max:
    jump = st.slider("ジャンプ（-1=開始前）", jump_min, jump_max, idx)
    if jump != idx:
        st.session_state.hl_idx = jump
        idx = jump


# ==== 概要メトリクス ====
if idx == -1 or not rounds:
    chips_now = init_chips
    remaining = len(deck)
    shown_round = 0
else:
    chips_now = rounds[idx]["chips_after"]
    remaining = len(rounds[idx]["remaining_deck"])
    shown_round = rounds[idx]["round"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("ラウンド", f"{shown_round}/{total_rounds}")
c2.metric("所持チップ", chips_now)
c3.metric("残り札", remaining)
c4.metric("初期チップ", init_chips)

st.divider()


# ==== 表示パネル ====
if idx == -1:
    st.info("開始前：ベースカードは未公開です。▶️ Start を押すと Round1 を表示します。")
elif 0 <= idx < len(rounds):
    r = rounds[idx]
    st.subheader(f"Round {r['round']}")
    st.markdown(f"- ベースカード：**{r['base_card']}**")
    st.markdown(f"- プレイヤー宣言：**{r['player_choice']}**")
    st.markdown(f"- 結果カード：**{r['result_card']}**")
    st.markdown(f"- 勝敗：**{r['outcome']}**")
    st.markdown(f"- ベット：**{r['bet']}**")
    st.markdown(f"- ラウンド後チップ：**{r['chips_after']}**")

# ==== ラウンド履歴（個別表示） ====
if rounds:
    st.divider()
    st.subheader("ラウンド履歴（個別）")
    for i, r in enumerate(rounds):
        with st.expander(f"Round {r['round']}", expanded=(i==idx)):
            st.markdown(f"<span style='font-size:1.5em; color:#e74c3c; font-weight:bold;'>ベースカード：{r['base_card']}</span>", unsafe_allow_html=True)
            st.markdown(f"- プレイヤー宣言：**{r['player_choice']}**")
            st.markdown(f"- 結果カード：**{r['result_card']}**")
            st.markdown(f"- 勝敗：**{r['outcome']}**")
            st.markdown(f"- ベット：**{r['bet']}**")
            st.markdown(f"- ラウンド後チップ：**{r['chips_after']}**")

st.divider()


# ==== 履歴（全体確認用） ====
st.subheader("履歴（全ラウンド）")
if rounds:
    df = pd.DataFrame(rounds)[
        ["round", "base_card", "player_choice", "result_card", "bet", "outcome", "chips_after"]
    ].rename(columns={
        "round": "ラウンド", "base_card": "ベース", "player_choice": "宣言",
        "result_card": "結果", "bet": "ベット", "outcome": "勝敗", "chips_after": "チップ"
    })
else:
    df = pd.DataFrame(columns=["ラウンド", "ベース", "宣言", "結果", "ベット", "勝敗", "チップ"])
st.dataframe(df, use_container_width=True)

if status.get("game_end"):
    st.caption(f"終了: {status['game_end']}")
