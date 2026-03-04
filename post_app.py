import streamlit as st
import pandas as pd

# --- 強制深色模式 CSS 與網頁設定 ---
st.set_page_config(page_title="甲佣試算一覽表", layout="centered")
st.markdown("""
<style>
    /* 整體背景與主要文字顏色 */
    .stApp { 
        background-color: #0E1117; 
        color: #FAFAFA; 
    }
    
    /* 🚫 【圖一修復】群組摺疊面板 (Expander) 標題列：強制深色，取消 hover 反白 */
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

    /* 🚫 【圖一修復】輸入保費框 (Number Input) & 選擇商品框 (Selectbox) 外觀：強制深色 */
    div[data-baseweb="input"],
    div[data-baseweb="input"]:hover,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:focus-within {
        background-color: #1E293B !important;
        border: 1px solid #475569 !important;
    }
    
    /* 輸入框裡面的文字 */
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] span {
        background-color: transparent !important;
        color: #FAFAFA !important;
        -webkit-text-fill-color: #FAFAFA !important;
    }
    
    /* 輸入框的加減按鈕 */
    div[data-baseweb="input"] button {
        background-color: transparent !important;
        color: #FAFAFA !important;
    }

    /* 讓輸入框標題 (label) 顯示淺灰色 */
    label p {
        color: #94A3B8 !important; 
        font-size: 14px !important;
    }

    /* 🚫 【圖二修復】下拉選單 "展開後的整串清單"：強制深色 */
    /* 因為下拉清單是浮動元件，必須用 role 屬性全域捕捉 */
    ul[role="listbox"], 
    div[data-baseweb="popover"] ul {
        background-color: #1E293B !important;
    }
    
    /* 清單內的每一列選項 */
    li[role="option"],
    div[data-baseweb="popover"] li {
        background-color: #1E293B !important;
        color: #FAFAFA !important;
    }
    
    /* 滑鼠停留在選項上時，稍微變淺一點點的深灰色 (不要變白) */
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #334155 !important; 
        color: #FAFAFA !important;
    }

    /* 微調分隔線顏色 */
    hr {
        border-color: #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 資料讀取區 ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO39goSGn2bbknXdW9m5t-S2EFb2ZdXDy75NJUUfL5vU8orEi7pzK9V3Ttp70tNQ/pub?output=csv"

@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_csv(SHEET_URL)
    df["甲佣比率(%)"] = df["甲佣比率(%)"].astype(str).str.replace('%', '').astype(float)
    if '發放' not in df.columns:
        df['發放'] = '100'
    if '換算係數' not in df.columns:
        df['換算係數'] = 0.088
    return df

df = load_data()

# --- 網頁標題與註解區 ---
st.title("📮 甲佣試算一覽表")

st.markdown("""
<div style='font-size: 14px; color: #94A3B8; line-height: 1.5; margin-bottom: 15px;'>
製作者：徐杰　v115.03.04_V3（修正版）<br>
甲佣比率請以最新公告之公文為主(壽字第1152200308號函)<br>
（本網頁僅供參考） 
</div>
<div style='display: flex; align-items: center; font-size: 15px; color: #94A3B8; margin-bottom: 20px; font-weight: bold;'>
    <span style='margin-right: 8px;'>👁️ 瀏覽人次：</span>
    <img src="https://hits.sh/post-commission-app-v1.streamlit.app.svg?label=累計&color=d97706&labelColor=334155" alt="views"/>
</div>
""", unsafe_allow_html=True)


# --- 試算介面邏輯 ---
groups = df["群組"].unique()

for group in groups:
    group_df = df[df["群組"] == group]
    count = len(group_df)
    
    with st.expander(f"{group} 　({count} 筆)", expanded=False):
        
        selected_product = st.selectbox(
            "選擇商品", 
            group_df["商品名稱"], 
            key=f"prod_{group}",
            label_visibility="collapsed"
        )
        
        row = group_df[group_df["商品名稱"] == selected_product].iloc[0]
        commission_rate = row["甲佣比率(%)"]
        
        try:
            factor = float(row['換算係數'])
            if pd.isna(factor) or factor == 0:
                factor = 0.088
        except:
            factor = 0.088
        
        payout_str = str(row['發放'])
        if payout_str == 'nan' or not payout_str.strip():
            payout_str = '100'
            
        try:
            payouts = [float(x.strip()) for x in payout_str.split(',')]
        except:
            payouts = [100.0]
        
        # --- 顯示上半部：商品標籤與比率 ---
        header_html = f"<div style='margin-bottom: 15px; margin-top: 5px;'><div style='font-size: 14px; color: #94A3B8; margin-bottom: 8px;'><span style='background-color: #FEF3C7; color: #D97706; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 8px;'>甲佣試算</span><span style='color:#FAFAFA; font-weight:bold; font-size: 15px;'>{selected_product}</span></div><div style='font-size: 16px; font-weight: bold; color: #FAFAFA;'>甲佣比率 <span style='color: #FBBF24; font-size: 20px;'>{commission_rate}%</span></div></div>"
        st.markdown(header_html, unsafe_allow_html=True)
        
        # --- 輸入保費框 ---
        premium = st.number_input("輸入保費 (月繳)", min_value=0, value=0, step=1000, key=f"prem_{group}")
        
        # 🏆 【核心公式修正區】
        exact_total = (premium / factor) * (commission_rate / 100)
        
        # --- 顯示下半部：分年期計算明細卡片 ---
        rows_html = "<div style='margin-top: 15px; background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 15px;'>"
        
        sum_yearly_amt = 0 
        
        for i, p in enumerate(payouts):
            amt = int((exact_total * (p / 100)) + 0.5)
            sum_yearly_amt += amt
            
            rows_html += f"<div style='display: flex; justify-content: space-between; padding: 6px 0; font-size: 15px;'><span style='color: #94A3B8;'>第{i+1}年 ({p}%)</span><span style='color: #FF4B4B; font-weight: bold;'>{amt:,} 元</span></div>"
            
        rows_html += f"<div style='display: flex; justify-content: space-between; padding-top: 12px; margin-top: 8px; border-top: 1px dashed #475569; font-size: 16px; font-weight: bold;'><span style='color: #FAFAFA;'>合計</span><span style='color: #FF4B4B;'>{sum_yearly_amt:,} 元</span></div></div>"
        
        st.markdown(rows_html, unsafe_allow_html=True)
