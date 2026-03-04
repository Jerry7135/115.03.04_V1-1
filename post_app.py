import streamlit as st
import pandas as pd

# --- 1. 網頁配置：分頁小圖示改用 Q 版郵筒圖片 ---
# 🎯 【修改點】page_icon 更新為 Q 版郵筒圖片網址
st.set_page_config(
    page_title="甲佣試算一覽表", 
    layout="centered", 
    page_icon="https://img.icons8.com/fluency/96/mailbox-closed-flag-down.png" 
)

# --- 強制深色模式 CSS 與網頁設定 ---
st.markdown("""
<style>
    /* 整體背景與主要文字顏色 */
    .stApp { 
        background-color: #0E1117; 
        color: #FAFAFA; 
    }
    
    /* 強制網頁大標題不換行，並根據螢幕自動縮放大小 */
    h1 {
        white-space: nowrap !important; 
        font-size: clamp(22px, 7vw, 40px) !important; 
    }
    
    /* 【標題與 Logo 設計】模仿圓角方塊效果 */
    .title-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
        white-space: nowrap;
    }
    .app-logo {
        background-color: #2563EB; /* 郵務藍色背景 */
        width: 60px;
        height: 60px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 2px solid #3B82F6;
        overflow: hidden; /* 確保圖片不超出圓角 */
        padding: 4px; /* 給圖片一點呼吸空間 */
    }
    /* 調整 Logo 圖片的樣式 */
    .app-logo img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain; /* 保持圖片比例並縮放適應 */
    }
    
    .main-title-text {
        font-size: clamp(26px, 7vw, 40px);
        font-weight: bold;
        color: #FAFAFA;
        margin: 0;
    }

    /* 群組摺疊面板 (Expander) 標題列 */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] details summary,
    [data-testid="stExpander"] details summary:hover,
    [data-testid="stExpander"] details summary:focus,
    [data-testid="stExpander"] details summary:active {
        background-color: #1E293B !important; 
        color: #FAFAFA !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }
    
    /* 摺疊面板展開後的內容區域背景 */
    [data-testid="stExpanderDetails"] {
        background-color: #0E1117; 
        border: 1px solid #334155;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }

    /* 選擇商品框箭頭變色 */
    div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
    }
    div[data-baseweb="select"] svg {
        fill: #FAFAFA !important;
    }

    /* 選擇商品後內容顏色變白 */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #FAFAFA !important;
    }

    /* 徹底鎖死輸入框反白 */
    .stNumberInput label p {
        color: #94A3B8 !important; 
        font-size: 14px !important;
    }
    [data-testid="stNumberInput"] div[data-baseweb="input"],
    [data-testid="stNumberInput"] div[data-baseweb="input"]:hover,
    [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
        background-color: #1E293B !important;
        border: 1px solid #475569 !important;
    }
    [data-testid="stNumberInput"] input {
        background-color: #1E293B !important;
        color: #FAFAFA !important;
        -webkit-text-fill-color: #FAFAFA !important; 
        caret-color: #FAFAFA !important; 
    }
    [data-testid="stNumberInput"] input::placeholder {
        color: #475569 !important;
    }
    [data-testid="stNumberInput"] button {
        display: none !important;
    }

    /* 清除按鈕 (x) 透明化 */
    [data-testid="stNumberInput"] div[data-baseweb="input"] > div {
        background-color: transparent !important;
    }
    [data-testid="stNumberInput"] div[data-baseweb="input"] [role="button"] {
        background-color: transparent !important;
    }
    [data-testid="stNumberInput"] div[data-baseweb="input"] svg {
        fill: #94A3B8 !important;
    }

    /* 下拉清單深色化 */
    ul[role="listbox"], div[data-baseweb="popover"] ul {
        background-color: #1E293B !important;
    }
    li[role="option"] {
        color: #FAFAFA !important;
    }
    li[role="option"]:hover {
        background-color: #334155 !important; 
    }

    hr { border-color: #334155 !important; }
</style>
""", unsafe_allow_html=True)

# --- 資料讀取區 ---
# 請確認這行網址是你原本的 CSV 公開網址，不要改動它
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQV5BqwNpncIYT0LB6bf67sGfMB0-dghenS23uGqX7WqLUo9qUv8PkG84JwQh58UmUlycRti-CKZErv/pub?output=csv"

@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_csv(SHEET_URL)
    df["甲佣比率(%)"] = df["甲佣比率(%)"].astype(str).str.replace('%', '').astype(float)
    if '發放' not in df.columns: df['發放'] = '100'
    if '換算係數' not in df.columns: df['換算係數'] = 0.088
    return df

df = load_data()

# --- 🎯 2. 標題區：嵌入可愛的 Q 版紅色郵筒圖片 Logo ---
# 我更換了一個更可愛的 Q 版郵筒圖片網址
st.markdown("""
<div class="title-container">
    <div class="app-logo">
        <img src="https://img.icons8.com/fluency/96/mailbox-closed-flag-down.png" alt="可愛郵筒">
    </div>
    <div class="main-title-text">甲佣試算一覽表</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='font-size: 14px; color: #94A3B8; line-height: 1.5; margin-bottom: 15px;'>
製作者：徐杰　v115.03.04_V13（可愛郵筒版）<br>
甲佣比率請以最新公告之公文為主(壽字第1152200308號函)<br>
（本網頁僅供參考） 
</div>
<div style='display: flex; align-items: center; font-size: 15px; color: #94A3B8; margin-bottom: 20px; font-weight: bold;'>
    <span style='margin-right: 8px;'>👁️ 瀏覽人次：</span>
    <img src="https://hits.sh/post-commission-app-v1.streamlit.app.svg?label=累計&color=d97706&labelColor=334155" alt="views"/>
</div>
""", unsafe_allow_html=True)

# --- 試算介面邏輯 (下方維持原樣，省略部分程式碼以節省空間) ---
groups = df["群組"].unique()

for group in groups:
    group_df = df[df["群組"] == group]
    count = len(group_df)
    
    with st.expander(f"{group} 　({count} 筆)", expanded=False):
        selected_product = st.selectbox("選擇商品", group_df["商品名稱"], key=f"prod_{group}", label_visibility="collapsed")
        row = group_df[group_df["商品名稱"] == selected_product].iloc[0]
        commission_rate = row["甲佣比率(%)"]
        
        try:
            factor = float(row['換算係數'])
            if pd.isna(factor) or factor == 0: factor = 0.088
        except: factor = 0.088
        
        payout_str = str(row['發放'])
        if payout_str == 'nan' or not payout_str.strip(): payout_str = '100'
        try: payouts = [float(x.strip()) for x in payout_str.split(',')]
        except: payouts = [100.0]
        
        header_html = f"<div style='margin-bottom: 15px; margin-top: 5px;'><div style='font-size: 14px; color: #94A3B8; margin-bottom: 8px;'><span style='background-color: #FEF3C7; color: #D97706; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 8px;'>甲佣試算</span><span style='color:#FAFAFA; font-weight:bold; font-size: 15px;'>{selected_product}</span></div><div style='font-size: 16px; font-weight: bold; color: #FAFAFA;'>甲佣比率 <span style='color: #FBBF24; font-size: 20px;'>{commission_rate}%</span></div></div>"
        st.markdown(header_html, unsafe_allow_html=True)
        
        premium = st.number_input("輸入保費 (月繳)", min_value=0, value=None, step=1000, key=f"prem_{group}", placeholder="請輸入金額")
        calc_premium = premium if premium is not None else 0
        exact_total = (calc_premium / factor) * (commission_rate / 100)
        
        rows_html = "<div style='margin-top: 15px; background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 15px;'>"
        sum_yearly_amt = 0 
        for i, p in enumerate(payouts):
            amt = int((exact_total * (p / 100)) + 0.5)
            sum_yearly_amt += amt
            rows_html += f"<div style='display: flex; justify-content: space-between; padding: 6px 0; font-size: 15px;'><span style='color: #94A3B8;'>第{i+1}年 ({p}%)</span><span style='color: #FF4B4B; font-weight: bold;'>{amt:,} 元</span></div>"
            
        rows_html += f"<div style='display: flex; justify-content: space-between; padding-top: 12px; margin-top: 8px; border-top: 1px dashed #475569; font-size: 16px; font-weight: bold;'><span style='color: #FAFAFA;'>合計</span><span style='color: #FF4B4B;'>{sum_yearly_amt:,} 元</span></div></div>"
        st.markdown(rows_html, unsafe_allow_html=True)
