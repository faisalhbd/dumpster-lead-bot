import os
import time
import hashlib
import logging
import requests
import feedparser

# ── Config ─────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")
CHECK_INTERVAL     = int(os.environ.get("CHECK_INTERVAL", "300"))

REPLY_TEMPLATE = (
    "Hi! I saw your post about dumpster rental. "
    "We have same-day roll-off dumpsters available in your area. "
    "Sizes: 10, 20, 30 & 40 yard. Best price guaranteed! "
    "Call/text us anytime for a free quote. What size do you need?"
)

# ── 150+ US Cities ──────────────────────────────────────────────────────────
CITIES = [
    # ── TIER 1: Major Metros ──────────────────────────────────────────────
    ("atlanta",         "Atlanta GA"),
    ("charlotte",       "Charlotte NC"),
    ("phoenix",         "Phoenix AZ"),
    ("dallas",          "Dallas TX"),
    ("tampa",           "Tampa FL"),
    ("houston",         "Houston TX"),
    ("orlando",         "Orlando FL"),
    ("nashville",       "Nashville TN"),
    ("denver",          "Denver CO"),
    ("lasvegas",        "Las Vegas NV"),
    ("austin",          "Austin TX"),
    ("sanantonio",      "San Antonio TX"),
    ("columbus",        "Columbus OH"),
    ("raleigh",         "Raleigh NC"),
    ("jacksonville",    "Jacksonville FL"),
    ("indianapolis",    "Indianapolis IN"),
    ("memphis",         "Memphis TN"),
    ("louisville",      "Louisville KY"),
    ("baltimore",       "Baltimore MD"),
    ("milwaukee",       "Milwaukee WI"),
    ("albuquerque",     "Albuquerque NM"),
    ("tucson",          "Tucson AZ"),
    ("fresno",          "Fresno CA"),
    ("sacramento",      "Sacramento CA"),
    ("kansascity",      "Kansas City MO"),
    ("omaha",           "Omaha NE"),
    ("cleveland",       "Cleveland OH"),
    ("minneapolis",     "Minneapolis MN"),
    ("tulsa",           "Tulsa OK"),
    ("wichita",         "Wichita KS"),
    ("neworleans",      "New Orleans LA"),
    ("richmond",        "Richmond VA"),
    ("batonrouge",      "Baton Rouge LA"),
    ("spokane",         "Spokane WA"),
    ("rochester",       "Rochester NY"),
    ("buffalo",         "Buffalo NY"),
    ("hartford",        "Hartford CT"),
    ("saltlakecity",    "Salt Lake City UT"),
    ("pittsburgh",      "Pittsburgh PA"),
    ("miami",           "Miami FL"),

    # ── TIER 2: Southeast ─────────────────────────────────────────────────
    ("knoxville",       "Knoxville TN"),
    ("chattanooga",     "Chattanooga TN"),
    ("columbia",        "Columbia SC"),
    ("greenville",      "Greenville SC"),
    ("charleston",      "Charleston SC"),
    ("savannah",        "Savannah GA"),
    ("macon",           "Macon GA"),
    ("augusta",         "Augusta GA"),
    ("huntsville",      "Huntsville AL"),
    ("birmingham",      "Birmingham AL"),
    ("montgomery",      "Montgomery AL"),
    ("mobile",          "Mobile AL"),
    ("jackson",         "Jackson MS"),
    ("shreveport",      "Shreveport LA"),
    ("littlerock",      "Little Rock AR"),
    ("fayetteville",    "Fayetteville AR"),
    ("oklahomacity",    "Oklahoma City OK"),
    ("amarillo",        "Amarillo TX"),
    ("lubbock",         "Lubbock TX"),
    ("elpaso",          "El Paso TX"),
    ("corpuschristi",   "Corpus Christi TX"),
    ("waco",            "Waco TX"),
    ("killeen",         "Killeen TX"),
    ("tyler",           "Tyler TX"),
    ("fortworth",       "Fort Worth TX"),
    ("plano",           "Plano TX"),
    ("denton",          "Denton TX"),
    ("daytona",         "Daytona Beach FL"),
    ("pensacola",       "Pensacola FL"),
    ("fortmyers",       "Fort Myers FL"),
    ("sarasota",        "Sarasota FL"),
    ("gainesville",     "Gainesville FL"),
    ("tallahassee",     "Tallahassee FL"),
    ("lakeland",        "Lakeland FL"),
    ("westpalmbeach",   "West Palm Beach FL"),
    ("fortlauderdale",  "Fort Lauderdale FL"),
    ("naples",          "Naples FL"),

    # ── TIER 2: Midwest ───────────────────────────────────────────────────
    ("cincinnati",      "Cincinnati OH"),
    ("akron",           "Akron OH"),
    ("toledo",          "Toledo OH"),
    ("dayton",          "Dayton OH"),
    ("grandrapids",     "Grand Rapids MI"),
    ("lansing",         "Lansing MI"),
    ("detroit",         "Detroit MI"),
    ("annarbor",        "Ann Arbor MI"),
    ("madison",         "Madison WI"),
    ("greenbay",        "Green Bay WI"),
    ("chicago",         "Chicago IL"),
    ("peoria",          "Peoria IL"),
    ("rockford",        "Rockford IL"),
    ("desmoines",       "Des Moines IA"),
    ("cedarrapids",     "Cedar Rapids IA"),
    ("lincoln",         "Lincoln NE"),
    ("stlouis",         "St Louis MO"),
    ("evansville",      "Evansville IN"),
    ("fortwayne",       "Fort Wayne IN"),
    ("southbend",       "South Bend IN"),

    # ── TIER 2: West ──────────────────────────────────────────────────────
    ("portland",        "Portland OR"),
    ("eugene",          "Eugene OR"),
    ("salem",           "Salem OR"),
    ("seattle",         "Seattle WA"),
    ("tacoma",          "Tacoma WA"),
    ("bellingham",      "Bellingham WA"),
    ("boise",           "Boise ID"),
    ("reno",            "Reno NV"),
    ("provo",           "Provo UT"),
    ("ogden",           "Ogden UT"),
    ("flagstaff",       "Flagstaff AZ"),
    ("scottsdale",      "Scottsdale AZ"),
    ("coloradosprings", "Colorado Springs CO"),
    ("fortcollins",     "Fort Collins CO"),
    ("aurora",          "Aurora CO"),
    ("boulder",         "Boulder CO"),

    # ── TIER 3: Small Markets (Low competition!) ──────────────────────────
    ("brunswick",       "Brunswick GA"),
    ("valdosta",        "Valdosta GA"),
    ("dothan",          "Dothan AL"),
    ("gulfport",        "Gulfport MS"),
    ("hattiesburg",     "Hattiesburg MS"),
    ("jonesboro",       "Jonesboro AR"),
    ("fortsmith",       "Fort Smith AR"),
    ("texarkana",       "Texarkana TX"),
    ("abilene",         "Abilene TX"),
    ("midland",         "Midland TX"),
    ("odessa",          "Odessa TX"),
    ("brownsville",     "Brownsville TX"),
    ("clarksville",     "Clarksville TN"),
    ("murfreesboro",    "Murfreesboro TN"),
    ("johnsoncity",     "Johnson City TN"),
    ("lexington",       "Lexington KY"),
    ("bowlinggreen",    "Bowling Green KY"),
    ("springfieldmo",   "Springfield MO"),
    ("pueblo",          "Pueblo CO"),
    ("henderson",       "Henderson NV"),
    ("olympia",         "Olympia WA"),
    ("medford",         "Medford OR"),
    ("yakima",          "Yakima WA"),
    ("richland",        "Richland WA"),
    ("idahofalls",      "Idaho Falls ID"),
    ("pocatello",       "Pocatello ID"),
    ("missoula",        "Missoula MT"),
    ("billings",        "Billings MT"),
    ("greatfalls",      "Great Falls MT"),
    ("casper",          "Casper WY"),
    ("cheyenne",        "Cheyenne WY"),
    ("rapid city",      "Rapid City SD"),
    ("siouxfalls",      "Sioux Falls SD"),
    ("fargo",           "Fargo ND"),
    ("bismarck",        "Bismarck ND"),
]

# ── Buy Intent Keywords ────────────────────────────────────────────────────
BUY_KEYWORDS = [
    "need dumpster", "rent dumpster", "looking for dumpster",
    "dumpster rental", "roll off", "rolloff", "junk removal",
    "debris removal", "cleanout", "clean out", "renovation",
    "roofing", "construction cleanup", "yard waste", "trash removal",
    "how much", "price", "quote", "asap", "urgent", "cheap dumpster",
    "10 yard", "20 yard", "30 yard", "40 yard", "bin rental",
    "waste removal", "haul away", "demo cleanup", "dumpster needed",
]

seen_ids: set = set()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def build_feeds(subdomain: str, label: str):
    base = f"https://{subdomain}.craigslist.org"
    # Combined OR query — max coverage, single request per section
    wanted_query = (
        "dumpster+rental"
        "+OR+dumpster+needed"
        "+OR+roll+off+container"
        "+OR+junk+removal"
        "+OR+debris+removal"
        "+OR+trash+hauling"
        "+OR+waste+removal"
        "+OR+cleanout+service"
        "+OR+yard+waste+removal"
        "+OR+construction+debris"
    )
    services_query = (
        "dumpster+rental"
        "+OR+roll+off"
        "+OR+junk+removal"
        "+OR+debris+removal"
    )
    return [
        (f"{label} [WANTED]",   f"{base}/search/wts?query={wanted_query}&format=rss"),
        (f"{label} [SERVICES]", f"{base}/search/sss?query={services_query}&format=rss"),
    ]


def send_telegram(message: str, reply_markup=None) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log.warning("Telegram credentials not set.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id":                  TELEGRAM_CHAT_ID,
        "text":                     message,
        "parse_mode":               "HTML",
        "disable_web_page_preview": False,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        log.error(f"Telegram error: {e}")
        return False


def score_entry(title: str, summary: str) -> int:
    text = (title + " " + summary).lower()
    score = sum(1 for kw in BUY_KEYWORDS if kw in text)
    if any(w in text for w in ["asap", "urgent", "today", "tomorrow", "immediately", "right away"]):
        score += 3
    if any(w in text for w in ["how much", "price", "quote", "cost", "rate"]):
        score += 2
    if any(w in text for w in ["need", "looking for", "wanted", "require"]):
        score += 2
    return score


def heat_label(score: int) -> str:
    if score >= 5:   return "🔥🔥🔥 HOT LEAD"
    elif score >= 3: return "🔥🔥 Warm Lead"
    elif score >= 1: return "🔥 Possible Lead"
    else:            return "👀 Monitor"


def check_feed(label: str, url: str) -> int:
    alerts = 0
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        log.error(f"Feed error [{label}]: {e}")
        return 0

    for entry in feed.entries:
        uid = entry.get("id") or hashlib.md5(entry.get("link", "").encode()).hexdigest()
        if uid in seen_ids:
            continue
        seen_ids.add(uid)

        title   = entry.get("title", "No title")
        link    = entry.get("link", "")
        summary = entry.get("summary", "")
        pub     = entry.get("published", "")

        score = score_entry(title, summary)
        if score == 0:
            continue

        heat = heat_label(score)

        msg = (
            f"{heat}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>{label}</b>\n"
            f"📌 <b>{title}</b>\n"
            f"🕐 {pub}\n"
            f"🔗 <a href='{link}'>View Post</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 Score: {score} | Reply within 5 min!"
        )

        # ── Inline buttons ────────────────────────────────────────────────
        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "📋 Copy Reply Template",
                        "callback_data": f"copy_reply"
                    },
                    {
                        "text": "🔗 Open Post",
                        "url": link
                    }
                ],
                [
                    {
                        "text": "✅ Lead Taken",
                        "callback_data": "lead_taken"
                    },
                    {
                        "text": "❌ Not Relevant",
                        "callback_data": "not_relevant"
                    }
                ]
            ]
        }

        log.info(f"ALERT [{label}]: {title} (score={score})")
        send_telegram(msg, reply_markup=reply_markup)
        alerts += 1
        time.sleep(0.5)

    return alerts


def handle_callback_query(update: dict):
    """Handle button taps from Telegram."""
    callback = update.get("callback_query", {})
    if not callback:
        return

    query_id   = callback.get("id")
    query_data = callback.get("data", "")
    chat_id    = callback.get("message", {}).get("chat", {}).get("id")

    # Answer the callback (removes loading spinner)
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery",
        json={"callback_query_id": query_id},
        timeout=5
    )

    if query_data == "copy_reply":
        # Send the reply template as a separate message (easy to copy)
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id":    chat_id,
                "text":       f"📋 <b>Reply Template:</b>\n\n<code>{REPLY_TEMPLATE}</code>\n\n👆 Tap to copy, then paste on Craigslist!",
                "parse_mode": "HTML",
            },
            timeout=5
        )
    elif query_data == "lead_taken":
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": "✅ Great! Good luck closing this lead! 💪"},
            timeout=5
        )
    elif query_data == "not_relevant":
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": "❌ Got it. Skipped."},
            timeout=5
        )


def poll_telegram_updates():
    """Long-poll Telegram for button taps."""
    offset = None
    while True:
        try:
            params = {"timeout": 10, "allowed_updates": ["callback_query"]}
            if offset:
                params["offset"] = offset
            r = requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                params=params,
                timeout=15
            )
            data = r.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                handle_callback_query(update)
        except Exception as e:
            log.error(f"Polling error: {e}")
        time.sleep(1)


def run():
    import threading

    total_feeds = len(CITIES) * 2  # 1 wanted (OR query) + 1 services (OR query)
    log.info(f"🚀 Bot started — {len(CITIES)} cities, {total_feeds} feeds.")

    send_telegram(
        f"🚀 <b>Dumpster Lead Bot v2 LIVE</b>\n"
        f"📍 <b>{len(CITIES)} US cities</b> monitoring\n"
        f"📡 Total feeds: <b>{total_feeds}</b>\n"
        f"⏱ Check every: <b>{CHECK_INTERVAL // 60} min</b>\n"
        f"🎯 Services + Wanted sections\n"
        f"📋 Reply template button enabled\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Hunting for leads... 🔥"
    )

    # Start Telegram button listener in background thread
    t = threading.Thread(target=poll_telegram_updates, daemon=True)
    t.start()

    cycle = 0
    while True:
        cycle += 1
        total_alerts = 0
        log.info(f"── Cycle #{cycle} started ({len(CITIES)} cities) ──")

        for subdomain, label in CITIES:
            for feed_label, feed_url in build_feeds(subdomain, label):
                count = check_feed(feed_label, feed_url)
                total_alerts += count
                time.sleep(1.2)

        log.info(f"Cycle #{cycle} complete. {total_alerts} new alerts.")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
