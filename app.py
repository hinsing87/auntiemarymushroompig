import random
import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="Auntie Mary 蘑菇豬大暴走", page_icon="🐷", layout="centered"
)

# 自訂 CSS 放大按鈕同文字，專為 iPad 觸控而設
st.markdown(
    """
    <style>
    .big-title { 
        font-size: 36px !important; 
        text-align: center; 
        color: #ff4757; 
        font-weight: bold; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button { 
        width: 100%; 
        height: 110px; 
        font-size: 28px; 
        font-weight: bold; 
        background-color: #2ed573; 
        color: white; 
        border-radius: 25px; 
        border: none; 
        box-shadow: 0px 6px 12px rgba(0,0,0,0.15);
    }
    .stButton>button:hover { 
        background-color: #26af5f; 
    }
    .reset-btn>button {
        background-color: #ffa502 !important;
        height: 70px !important;
        font-size: 20px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 遊戲標題
st.markdown(
    '<p class="big-title">🍄 Auntie Mary 蘑菇豬大暴走 🐷</p>',
    unsafe_allow_html=True,
)
st.write(
    "<h4 style='text-align: center; color: #747d8c;'>4歲小朋友嘅專屬瘋狂派對！</h4>",
    unsafe_allow_html=True,
)
st.write("")

# 初始化狀態
if "score" not in st.session_state:
    st.session_state.score = 0
if "action_idx" not in st.session_state:
    st.session_state.action_idx = 0
if "character_icon" not in st.session_state:
    st.session_state.character_icon = "🐷"

# 搞笑又過癮嘅隨機事件庫
funny_events = [
    ("🐷", "蘑菇豬一口吞咗個大蘑菇，個肚滾下滾下！"),
    ("💃", "Auntie Mary 同蘑菇豬一齊跳森巴舞！"),
    ("⚡", "蘑菇豬食完變左超級撒亞豬，飛上天呀！"),
    ("🌀", "哎呀！跣咗個斗，轉左三個圈！"),
    ("💖", "Auntie Mary 派左個心心比全場小朋友！"),
    ("🌟", "執到隱藏嘅七彩金蘑菇，賺到笑！"),
]

# 顯示大公仔
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        "<h1 style='text-align: center; font-size: 60px;'>👩‍🍳</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>Auntie Mary</p>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"<h1 style='text-align: center; font-size: 60px;'>{st.session_state.character_icon}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>蘑菇豬</p>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        "<h1 style='text-align: center; font-size: 60px;'>🍄</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>美味蘑菇</p>",
        unsafe_allow_html=True,
    )

st.write("---")

# 狂野大按鈕
if st.button("🚀 勁大力禁：餵豬豬食蘑菇！ 🚀"):
    st.session_state.score += 1
    # 隨機揀一個搞笑事件
    st.session_state.action_idx = random.randint(0, len(funny_events) - 1)
    st.session_state.character_icon, _ = funny_events[
        st.session_state.action_idx
    ]

    # 每食 5 個蘑菇有超級慶祝
    if st.session_state.score % 5 == 0:
        st.balloons()

# 顯示即時戰績與搞鬼對白
st.write("")
score_label = f"<h2 style='text-align: center; color: #1e90ff;'>豬豬已經食咗 <b>{st.session_state.score}</b> 個蘑菇啦！</h2>"
st.markdown(score_label, unsafe_allow_html=True)

_, current_text = funny_events[st.session_state.action_idx]
dialogue_box = f"<h3 style='text-align: center; color: #ff4757; background-color: #f1f2f6; padding: 15px; border-radius: 15px;'>{current_text}</h3>"
st.markdown(dialogue_box, unsafe_allow_html=True)

# 底部重設按鈕
st.write("")
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    if st.button("🔄 重新玩過", key="reset"):
        st.session_state.score = 0
        st.session_state.action_idx = 0
        st.session_state.character_icon = "🐷"
        st.rerun()
