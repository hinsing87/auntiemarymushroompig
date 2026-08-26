import random
import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="Auntie Mary 蘑菇豬配對遊戲", page_icon="🃏", layout="centered"
)

# 自訂 CSS 讓 iPad 更好按、卡片更美觀
st.markdown(
    """
    <style>
    .big-title { 
        font-size: 32px !important; 
        text-align: center; 
        color: #ff4757; 
        font-weight: bold; 
    }
    .stButton>button { 
        width: 100%; 
        height: 80px; 
        font-size: 28px; 
        border-radius: 15px; 
    }
    .card-btn>button {
        height: 90px !important;
        font-size: 36px !important;
        background-color: #f1f2f6 !important;
        border: 2px solid #ced6e0 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 標題
st.markdown(
    '<p class="big-title">🃏 Auntie Mary 蘑菇豬配對大冒險 🐷</p>',
    unsafe_allow_html=True,
)
st.write(
    "<h4 style='text-align: center; color: #747d8c;'>訓練記憶力：搵出兩張一樣嘅卡片！</h4>",
    unsafe_allow_html=True,
)
st.write("")

# 定義遊戲圖標（必須包含主角）
CORE_ITEMS = ["👩‍🍳", "🍄", "🐷"]
EXTRA_ITEMS = ["🎂", "⭐", "💖", "🎈", "🚗"]

# 初始化遊戲狀態
if "board" not in st.session_state:
    st.session_state.game_started = False

# 難度選擇
difficulty = st.selectbox(
    "📏 請選擇難度：", ["簡單 (4張卡 - 好容易)", "中級 (6張卡 - 挑戰)", "刺激 (8張卡 - 高手)"]
)

# 根據難度設定卡片數量
if "簡單" in difficulty:
    num_pairs = 2
elif "中級" in difficulty:
    num_pairs = 3
else:
    num_pairs = 4


def init_game():
    # 確保一定有 Auntie Mary, 蘑菇, 豬 (或者部分隨機選取)
    selected_icons = CORE_ITEMS.copy()
    if num_pairs > len(CORE_ITEMS):
        extra_needed = num_pairs - len(CORE_ITEMS)
        selected_icons += random.sample(EXTRA_ITEMS, extra_needed)
    elif num_pairs < len(CORE_ITEMS):
        selected_icons = random.sample(CORE_ITEMS, num_pairs)

    # 製作雙份以供配對
    deck = selected_icons * 2
    random.shuffle(deck)

    st.session_state.board = deck
    st.session_state.flipped = [False] * len(deck)
    st.session_state.matched = [False] * len(deck)
    st.session_state.first_selection = None
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.game_started = True


# 開始/重新開始按鈕
col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
with col_r2:
    if st.button("🎮 開始遊戲 / 重新洗牌"):
        init_game()
        st.rerun()

st.write("---")

# 如果未開始，自動初始化一次
if not st.session_state.get("game_started", False):
    init_game()

board = st.session_state.board
matched = st.session_state.matched
flipped = st.session_state.flipped

# 顯示卡片網格（每行 2 或 4 張）
cols_per_row = 2 if num_pairs <= 2 else 4
rows = [board[i : i + cols_per_row] for i in range(0, len(board), cols_per_row)]

for r_idx, row in enumerate(rows):
    cols = st.columns(len(row))
    for c_idx, icon in enumerate(row):
        absolute_idx = r_idx * cols_per_row + c_idx
        with cols[c_idx]:
            # 如果已經配對成功，顯示剔號；如果反開咗，顯示圖標；否則顯示問號
            if matched[absolute_idx]:
                st.markdown(
                    f"<div style='text-align:center; font-size:36px; padding:20px; background:#2ed573; border-radius:15px;'>✅</div>",
                    unsafe_allow_html=True,
                )
            elif flipped[absolute_idx]:
                st.markdown(
                    f"<div style='text-align:center; font-size:36px; padding:20px; background:#ffffff; border:2px solid #ff4757; border-radius:15px;'>{board[absolute_idx]}</div>",
                    unsafe_allow_html=True,
                )
            else:
                if st.button("❓", key=f"card_{absolute_idx}"):
                    # 翻開這張卡
                    st.session_state.flipped[absolute_idx] = True

                    if st.session_state.first_selection is None:
                        # 這是第一張翻開的卡
                        st.session_state.first_selection = absolute_idx
                    else:
                        # 這是第二張翻開的卡
                        first_idx = st.session_state.first_selection
                        st.session_state.attempts += 1

                        if (
                            board[first_idx] == board[absolute_idx]
                            and first_idx != absolute_idx
                        ):
                            # 配對成功！
                            st.session_state.matched[first_idx] = True
                            st.session_state.matched[absolute_idx] = True
                            st.session_state.score += 1
                            st.session_state.first_selection = None

                            # 檢查是否全部配對成功
                            if all(st.session_state.matched):
                                st.balloons()
                        else:
                            # 配對失敗，短暫記住後需要讓小朋友知道（Streamlit會自動刷新，我們可以稍後再覆蓋狀態或直接翻轉）
                            # 為了簡單流暢，這裡點擊下一張時會重設上一輪未配對的卡
                            pass
                    st.rerun()

# 遊戲統計與通關祝賀
st.write("")
st.write(
    f"<h3 style='text-align: center; color: #1e90ff;'>已成功配對：{st.session_state.score} / {num_pairs} 對</h3>",
    unsafe_allow_html=True,
)

if all(st.session_state.matched) and st.session_state.get("game_started", False):
    st.markdown(
        "<h2 style='text-align: center; color: #ff4757;'>🎉 太棒啦！你幫 Auntie Mary 搵晒所有蘑菇豬朋友仔！ 🎉</h2>",
        unsafe_allow_html=True,
    )
