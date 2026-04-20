import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# 1. PAGE CONFIG
st.set_page_config(
    page_title="မြန်မာ ရွှေဈေး ခွဲခြမ်းစိတ်ဖြာမှု",
    page_icon="🥇",
    layout="wide",
)

# 2. DATA FETCHING FUNCTION (ERROR FIXED)
@st.cache_resource(ttl=300)
def fetch_gold_data():
    try:
        ticker = yf.Ticker("GC=F")
        # ခြောက်လစာ ဒေတာယူမယ်
        hist = ticker.history(period="6mo", interval="1d")
        
        if hist.empty:
            return None, None
            
        # Multi-index header ပြဿနာကို ရှင်းထုတ်ခြင်း
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)
            
        hist.index = pd.to_datetime(hist.index)
        
        # Live Price ယူခြင်း
        current_price = hist['Close'].iloc[-1]
        
        return hist, current_price
    except Exception as e:
        return None, None

# 3. SIDEBAR SETUP
with st.sidebar:
    st.title("🥇 ရွှေဈေးတွက်ချက်မှု")
    cbm_rate = st.number_input("ဗဟိုဘဏ်ဈေး (ကျပ်)", value=2100.0)
    market_rate = st.number_input("ပြင်ပပေါက်ဈေး (ကျပ်)", value=4500.0)
    rate_choice = st.radio("ဈေးနှုန်းရွေးချယ်ပါ", ["ဗဟိုဘဏ်နှုန်း", "ပြင်ပပေါက်ဈေး"])
    
    selected_rate = cbm_rate if rate_choice == "ဗဟိုဘဏ်နှုန်း" else market_rate

# 4. MAIN LOGIC
hist, gold_price = fetch_gold_data()

if hist is not None:
    # မြန်မာရွှေဈေး တွက်နည်း
    mm_gold_price = ((gold_price * 1.029) * selected_rate) / 0.576
    
    # UI Display
    st.header(f"🇲🇲 မြန်မာ့ရွှေဈေး: {mm_gold_price:,.0f} ကျပ်")
    
    col1, col2 = st.columns(2)
    col1.metric("ကမ္ဘာ့ရွှေဈေး (USD)", f"${gold_price:,.2f}")
    col2.metric("အသုံးပြုသည့် ဒေါ်လာဈေး", f"{selected_rate:,.0f} MMK")

    # 5. CHART
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                open=hist['Open'], high=hist['High'],
                low=hist['Low'], close=hist['Close'])])
    fig.update_layout(title="Gold Price Chart (6 Months)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # 6. SMC ANALYSIS (SIMPLE VERSION)
    st.subheader("🧠 SMC Analysis (တစ်နေ့တာ)")
    last_close = hist['Close'].iloc[-1]
    prev_close = hist['Close'].iloc[-2]
    
    if last_close > prev_close:
        st.success("Trend: Bullish (ဈေးတက်ရန် အလားအလာရှိသည်)")
    else:
        st.error("Trend: Bearish (ဈေးပြန်ကျနိုင်သည်)")
else:
    st.error("ဒေတာဆွဲယူ၍ မရပါ။ Internet Connection ကို စစ်ဆေးပြီး Refresh လုပ်ပေးပါ။")
