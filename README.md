# 🥇 Myanmar Gold Market Pro

**Live XAUUSD · SMC Analysis · Myanmar Gold Calculations**

Dark-themed professional dashboard combining live gold prices with Smart Money Concepts (SMC) technical analysis and Myanmar kyat/pael calculations.

---

## ✨ Features

| Feature | Details |
|---|---|
| 📡 Live Price | Binance XAUUSDT → Coinbase fallback (30s refresh) |
| 🇲🇲 Myanmar Calc | ကျပ်သား / ပဲသား / Gram · Market & CBM rates |
| 📈 Interactive Chart | Plotly candlestick · EMA 21/50/200 · Daily/Weekly/Monthly |
| 🎯 SMC Analysis | BOS · CHoCH · Order Blocks · Fair Value Gaps |
| 🔮 Predictions | Daily / Weekly / Monthly signal with R:R ratio |
| ⚖️ Multi-TF | 3-timeframe summary at a glance |

---

## 🚀 Deploy on Streamlit Cloud (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Myanmar Gold Pro v3.0"
git remote add origin https://github.com/YOUR_USERNAME/myanmar-gold-pro.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo → branch: `main` → file: `app.py`
5. Click **"Deploy"** ✅

Your app will be live at:
`https://YOUR_USERNAME-myanmar-gold-pro-app-XXXXX.streamlit.app`

---

## 📁 File Structure

```
myanmar_gold_app/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
├── .streamlit/
│   └── config.toml    ← Dark gold theme config
└── README.md
```

---

## 🧠 SMC Strategy Logic

| Concept | Description |
|---|---|
| **Swing H/L** | Pivot detection with configurable lookback |
| **BOS** | Break of Structure — trend continuation signal |
| **CHoCH** | Change of Character — potential reversal signal |
| **Order Blocks** | Supply/demand zones before impulse moves |
| **FVG** | Fair Value Gaps — 3-candle imbalance zones |
| **Premium/Discount** | Fibonacci 38.2% / 61.8% zone classification |
| **Signal Score** | Confluence-based 1–5 star rating |

---

## ⚠️ Disclaimer

SMC analysis is for **educational purposes only**.  
Not financial advice. Past performance ≠ future results.  
Always do your own due diligence before investing.

---

## 🛠️ Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

*Built with ❤️ for Myanmar Gold Traders*
