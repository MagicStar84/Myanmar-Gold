import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# ─────────────────────────────────────────────
#  PAGE CONFIG & CSS (အစ်ကို့မူရင်းအတိုင်း ထားရှိပါသည်)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="မြန်မာ ရွှေဈေး ခွဲခြမ်းစိတ်ဖြာမှု",
    page_icon="🥇",
    layout="wide",
)

# ... (အစ်ကို့ CSS code တွေ ဒီနေရာမှာ ရှိမယ်၊ နေရာလွတ်စေရန် ချန်လှပ်ထားပါသည်) ...
# (အောက်က Helper Functions အပိုင်းမှာ အဓိက ပြင်ဆင်ထားပါတယ်)

# ─────────────────────────────────────────────
#  UPDATED HELPER FUNCTIONS (FIXED ERROR)
# ─────────────────────────────────────────────

@st.cache_resource(ttl=300)  # Serialization Error အတွက် cache_resource ကို သုံးသည်
def fetch_gold_data():
    """Fetch live + historical gold data from Yahoo Finance with error handling."""
    try:
        ticker = yf.Ticker("GC=F")
        # ဒေတာဆွဲယူခြင်း
        hist = ticker.history(period="6mo", interval="1d")
        
        if hist.empty:
            return None, None
            
        # yfinance ရဲ့ Multi-index issue ကို ရှင်းရန် column အမည်များကို clean လုပ်ခြင်း
        hist.columns = [col[0] if isinstance(col, tuple) else col for col in hist.columns]
        
        # ဒေတာကို sorting ပြန်လုပ်ပြီး index ကို datetime အဖြစ် သေချာအောင်လုပ်ခြင်း
        hist.index = pd.to_datetime(hist.index)
        
        # Fast Info (Price) ယူခြင်း
        info = ticker.fast_info
        current_price = info['last_price'] if 'last_price' in info else hist['Close'].iloc[-1]
        
        return hist, current_price
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None

def calc_myanmar_gold(gold_usd: float, usd_rate: float) -> float:
    """((Gold_Price * 1.029) * USD_Rate) / 0.576"""
    return ((gold_usd * 1.029) * usd_rate) / 0.576

# ... (smc_analysis function နှင့် အခြား UI code များ အစ်ကို့မူရင်းအတိုင်း ဆက်ရှိပါမည်) ...

# ─────────────────────────────────────────────
#  MAIN CONTENT (FIXED DATA LOADING)
# ─────────────────────────────────────────────

# Fetch data using updated logic
with st.spinner("ရွှေဈေးနှုန်း ဆွဲနေသည်..."):
    hist, live_gold_price = fetch_gold_data()
    data_ok = hist is not None and not hist.empty

if not data_ok:
    st.warning("ဈေးနှုန်းဒေတာ မရရှိပါ။ Internet ချိတ်ဆက်မှု သို့မဟုတ် API Limit ကို စစ်ဆေးပါ။")
    st.stop()

# ကျန်တဲ့ UI code တွေကို အစ်ကို့မူရင်းအတိုင်း ဆက်သုံးနိုင်ပါတယ်
# gold_price နေရာမှာ live_gold_price ကို အသုံးပြုထားပါသည်
