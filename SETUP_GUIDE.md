# 🗑️ Dumpster Lead Bot v3 — Full Setup Guide

---

## কি কি লাগবে (সব FREE)
- GitHub account → github.com
- Railway account → railway.app
- Telegram account

---

## STEP 1 — Telegram Bot বানাও (৩ মিনিট)

### 1.1 Bot Token নাও
1. Telegram এ search করো: **@BotFather**
2. Start বাটন চাপো
3. লিখো: `/newbot`
4. Bot এর নাম দাও: `Dumpster Lead Bot`
5. Username দাও: `dumpster_lead_yourname_bot`
6. BotFather একটা token দেবে এরকম:
   ```
   1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
   ```
7. এটা copy করে রাখো → এটাই `TELEGRAM_BOT_TOKEN`

### 1.2 Chat ID নাও
1. Telegram এ search করো: **@userinfobot**
2. Start বাটন চাপো
3. তোমার ID দেখাবে এরকম: `123456789`
4. এটা copy করো → এটাই `TELEGRAM_CHAT_ID`

### 1.3 Bot কে Start করো
1. তোমার নতুন bot এ যাও (username দিয়ে search করো)
2. **Start** বাটন চাপো
   ⚠️ এটা না করলে bot message পাঠাতে পারবে না!

---

## STEP 2 — GitHub Repo বানাও (২ মিনিট)

1. **github.com** এ login করো
2. উপরে **"+"** বাটন → **"New repository"**
3. Repository name: `dumpster-lead-bot`
4. **Public** রাখো
5. **"Create repository"** চাপো
6. এখন ZIP file extract করো তোমার computer এ
7. এই ৪টা file GitHub এ upload করো:
   - `monitor.py`
   - `requirements.txt`
   - `Procfile`
   - `.env.example`

### GitHub এ upload করতে:
1. Repo page এ **"uploading an existing file"** link চাপো
2. ৪টা file drag & drop করো
3. **"Commit changes"** চাপো ✅

---

## STEP 3 — Railway Deploy করো (৫ মিনিট)

### 3.1 Railway Account
1. **railway.app** এ যাও
2. **"Login"** → **"Login with GitHub"**
3. GitHub দিয়ে connect করো

### 3.2 New Project বানাও
1. Dashboard এ **"New Project"** চাপো
2. **"Deploy from GitHub repo"** চাপো
3. তোমার `dumpster-lead-bot` repo select করো
4. **"Deploy Now"** চাপো

### 3.3 Environment Variables সেট করো
1. Project খুললে উপরে **"Variables"** tab এ যাও
2. **"New Variable"** চাপো, একটা একটা করে add করো:

| Variable Name | Value |
|---------------|-------|
| `TELEGRAM_BOT_TOKEN` | তোমার bot token (Step 1.1 থেকে) |
| `TELEGRAM_CHAT_ID` | তোমার chat id (Step 1.2 থেকে) |
| `CHECK_INTERVAL` | `300` |

3. Variables save হলে Railway automatically **redeploy** করবে

### 3.4 Worker সেট করো
1. **"Settings"** tab এ যাও
2. **"Service"** section এ দেখো
3. Railway নিজেই `Procfile` detect করে worker চালাবে ✅

---

## STEP 4 — Verify করো

1. Railway এর **"Logs"** tab এ যাও
2. এরকম দেখাবে:
   ```
   🚀 Bot started — 135 cities, 270 feeds.
   ── Cycle #1 started ──
   ```
3. তোমার Telegram এ message আসবে:
   ```
   🚀 Dumpster Lead Bot v3 LIVE
   📍 135 US cities monitoring...
   ```

✅ **Bot live!**

---

## কিভাবে Alert দেখাবে

```
🔥🔥🔥 HOT LEAD
━━━━━━━━━━━━━━━━━━━━
📍 Atlanta GA [WANTED]
📌 Need 20 yard dumpster asap for renovation
🕐 Mon, 14 Apr 2025 09:23:11
🔗 View Post
━━━━━━━━━━━━━━━━━━━━
💡 Score: 7 | Reply within 5 min!

[📋 Copy Reply Template]  [🔗 Open Post]
[✅ Lead Taken]           [❌ Not Relevant]
```

### Button এর কাজ:
- **📋 Copy Reply Template** → Ready-made reply message আসবে, copy করে post এ paste করো
- **🔗 Open Post** → Craigslist post সরাসরি খুলবে
- **✅ Lead Taken** → Mark করো যে তুমি contact করেছো
- **❌ Not Relevant** → Skip করো

---

## Secret Tips 🤫

### কখন reply করবে?
- Alert আসার **৫ মিনিটের মধ্যে** reply করো
- Close rate: **80%+** যদি first reply হও

### Peak Hours (EST):
```
☀️  8am  - 12pm  → সবচেয়ে বেশি post
🌤️  12pm - 5pm   → Moderate
🌙  5pm  - 8pm   → Low
```

### CHECK_INTERVAL কমাও peak hours এ:
- Normal: `300` (5 মিনিট)
- Peak:   `180` (3 মিনিট)

### [WANTED] feed মানে:
- কেউ actively dumpster খুঁজছে
- এগুলো সবচেয়ে hot leads — সাথে সাথে reply করো

### Tier 3 cities secret:
- ছোট শহরে competition প্রায় নাই
- Same demand, কম competition = easier close

---

## Troubleshooting

| সমস্যা | সমাধান |
|--------|--------|
| Telegram message আসছে না | Bot কে Start করেছো? (Step 1.3) |
| Railway crash করছে | Logs চেক করো, token ঠিক আছে? |
| কোনো alert নাই | Normal — post না থাকলে alert আসবে না |
| Too many alerts | `CHECK_INTERVAL=600` করো |

---

## Files
```
dumpster-bot-v3/
├── monitor.py        # Main bot
├── requirements.txt  # Dependencies
├── Procfile          # Railway config
└── .env.example      # Variables template
```
