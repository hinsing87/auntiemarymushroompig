import random
import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="Auntie Mary 蘑菇豬", page_icon="🍄", layout="centered"
)

# 自訂 CSS 放大文字同按鈕，方便4歲小朋友操作
st.markdown(
    """
    <style>
    .big-title { font-size: 38px !important; text-align: center; color: #ff6b6b; font-weight: bold; }
    .stButton>button { width: 100%; height: 90px; font-size: 26px; font-weight: bold; background-color: #ff9f43; color: white; border-radius: 20px; border: none; box-shadow: 0px 4px 6px rgba(0,0,0,0.2); }
    .stButton>button:hover { background-color: #ee5253; }
    </style>
""",
    unsafe_allow_html=True,
)

# 標題
html_title = '<p class="big-title">🍄 Auntie Mary 蘑菇豬 🐷</p>'
st.markdown(html_title, unsafe_allow_html=True)
st.write(
    "<h4 style='text-align: center; color: #576574;'>專為 4 歲小朋友而設嘅開心小遊戲！</h4>",
    unsafe_allow_html=True,
)
st.write("")

# 初始化遊戲分數同對話
if "score" not in st.session_state:
    st.session_state.score = 0
if "msg_idx" not in st.session_state:
    st.session_state.msg_idx = 0

# 趣致對白庫
phrases = [
    "Oink! 豬豬食咗個好味蘑菇！🍄",
    "Auntie Mary 笑得好開心！😄",
    "蘑菇豬喺度跳緊森巴舞呀！💃",
    "好好味呀！Encore Encore！👏",
    "Auntie Mary 畀左個大拇指👍！",
]

# 顯示可愛公仔圖示
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        "<h1 style='text-align: center;'>👩‍🍳</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>Auntie Mary</p>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        "<h1 style='text-align: center;'>🐷</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>蘑菇豬</p>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        "<h1 style='text-align: center;'>🍄</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>新鮮蘑菇</p>",
        unsafe_allow_html=True,
    )

st.write("---")

# 互動大按鈕
if st.button("🌟 禁呢度：餵蘑菇豬食嘢！ 🌟"):
    st.session_state.score += 1
    st.session_state.msg_idx = random.randint(0, len(phrases) - 1)
    # 每食 5 個蘑菇放出汽球慶祝
    if st.session_state.score % 5 == 0:
        st.balloons()

# 顯示分數同對白
st.write("")
score_text = f"<h2 style='text-align: center; color: #2e86de;'>豬豬已經食咗 {st.session_state.score} 個蘑菇啦！</h2>"
st.markdown(score_text, unsafe_allow_html=True)

msg_text = f"<h3 style='text-align: center; color: #ee5253;'>{phrases[st.session_state.msg_idx]}</h3>"
st.markdown(msg_text, unsafe_allow_html=True)

# 底部重設掣
st.write("")
st.write("")
if st.button("🔄 重新開始"):
    st.session_state.score = 0
    st.rerun()
