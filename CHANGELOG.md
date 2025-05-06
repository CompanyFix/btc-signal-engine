
# 📘 CHANGELOG — Crypto AI Trader

This document records key decisions, features added, and structural changes during the development of the Crypto AI Trader platform.

---

## ✅ [Initial Setup] — May 6, 2025

- Project scope defined for Bitcoin AI-powered auto-trading tool
- Agreed on multi-timeframe (32+ timeframes) analysis structure
- Confirmed indicators: RSI, MACD, EMA, OBV, Volume, Fibonacci
- Established confidence scoring system (0%–100%)
- Defined trade strategy types: scalp, intraday, swing, long-term
- Bitget confirmed as the default exchange for API execution
- VPS hosting recommended for 24/7 uptime (DigitalOcean or similar)
- GitHub private repo structure outlined
- Modular Python-based architecture approved (data/indicators/models/etc.)

---

## 💡 [Strategic Additions] — May 6, 2025

- ✅ Added final step “visual sanity check” using TradingView screenshot to mimic human confirmation
- Planned dynamic adjustment of confidence score based on visual pattern detection
- Screenshot module to live at end of pipeline in `/visual_layer/`
- Visual analysis will override or reduce recommendation confidence if patterns conflict with indicator logic

---

## 🧠 Memory & Learning

- Assistant will retain core architecture, strategies, API decisions, and long-term goals
- User advised to keep log of specific custom scripts, formulas, and personal code changes
- `NOTES.md` and `CHANGELOG.md` will document development iterations moving forward

---
