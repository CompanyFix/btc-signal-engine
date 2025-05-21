# 📈 BTC Signal Engine

A real-time Bitcoin trading signal platform that uses multi-timeframe indicators and machine learning to generate high-confidence LONG/SHORT trade alerts.

## 🔧 Features

- ✅ Pulls real-time BTC/USDT data from TradingView via `tvDatafeed`
- ✅ Applies indicators: RSI, MACD, EMA, VWAP, Bollinger Bands
- ✅ Uses trained XGBoost models to predict direction + move tier
- ✅ Sends formatted alerts every 5 minutes via email-to-SMS or email
- ✅ Streamlit dashboard (coming soon)
- ✅ Fully version-controlled using GitHub

---

## 🗂️ Key Files

| File                            | Purpose                                 |
|---------------------------------|-----------------------------------------|
| `btc_signal_notifier.py`        | Main script that runs every 5 min       |
| `btc_signal_notifier_main_stable.py` | Backup of known working version   |
| `run_signal_once.py`            | One-time manual signal trigger          |
| `.env`                          | Email credentials + recipient gateway   |
| `.gitignore`                    | Prevents sensitive/large files in repo |

---

## 🧪 How to Run

### 🔁 Scheduled Loop
```bash
source venv/Scripts/activate
python btc_signal_notifier.py


>>>>>>> 4c75950068a0bae889f68c2ed50057071563d632
