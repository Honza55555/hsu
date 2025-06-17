import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

TOKEN    = os.environ["TELEGRAM_TOKEN"]
BASE_URL = os.environ["BASE_URL"]  # např. "https://coffee-perk.onrender.com"

bot = Bot(token=TOKEN)
dp  = Dispatcher(bot, None, workers=0, use_context=True)

app = Flask(__name__)


# ─── HANDLERY ────────────────────────────────────────────────────────────────

def start(update, context):
    """/start — pošle češtinu/angličtinu."""
    kb = [
        [
            InlineKeyboardButton("🇨🇿 Čeština", callback_data="lang_cs"),
            InlineKeyboardButton("🌍 English", callback_data="lang_en")
        ]
    ]
    update.message.reply_text(
        "☕️ Vítejte v Coffee Perk!\n"
        "We’re happy to see you here. 🌟\n"
        "Please choose your language. 🗣️",
        reply_markup=InlineKeyboardMarkup(kb)
    )

def menu_cs(update, context):
    """Čeština — hlavní nabídka."""
    kb = [
        [InlineKeyboardButton("🧾 Menu a nabídka", callback_data="m1")],
        [InlineKeyboardButton("🕐 Otevírací doba", callback_data="m2")],
        [InlineKeyboardButton("📍 Kde nás najdete", callback_data="m3")],
        [InlineKeyboardButton("📞 Kontakt / Rezervace", callback_data="m4")],
        [InlineKeyboardButton("📦 Předobjednávka (již brzy)", callback_data="m5")],
        [InlineKeyboardButton("😎 Proč si zajít na kávu", callback_data="m6")],
    ]
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Na co se mě můžeš zeptat:", reply_markup=InlineKeyboardMarkup(kb)
    )

def menu_en(update, context):
    """English — main menu."""
    kb = [
        [InlineKeyboardButton("🧾 Menu & Offer", callback_data="e1")],
        [InlineKeyboardButton("🕐 Opening Hours", callback_data="e2")],
        [InlineKeyboardButton("📍 Find Us", callback_data="e3")],
        [InlineKeyboardButton("📞 Contact / Booking", callback_data="e4")],
        [InlineKeyboardButton("📦 Pre-order Soon", callback_data="e5")],
        [InlineKeyboardButton("😎 Why Coffee?", callback_data="e6")],
    ]
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "What can I help you with?", reply_markup=InlineKeyboardMarkup(kb)
    )


CS_TEXT = {
    "m1": "🥐 **COFFEE PERK MENU ☕️**\n\n"
          "U nás nejde jen o kafe. Je to malý rituál. Je to nálada. Je to... láska v šálku. 💘\n\n"
          "☕ Výběrová káva\n"
          "🍳 Snídaně (lehké i pořádné)\n"
          "🍰 Domácí dorty\n"
          "🥗 Brunch a saláty\n\n"
          "📄 Kompletní menu:\n"
          "👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
          "Ať už si dáte espresso, matchu nebo zázvorovku – tady to chutná líp. 💛",
    "m2": "🕐 **KDY MÁME OTEVŘENO?**\n\n"
          "📅 Pondělí–Pátek: 7:30 – 17:00\n"
          "📅 Sobota & Neděle: ZAVŘENO\n\n"
          "Chcete nás navštívit? Jsme tu každý všední den od brzkého rána. ☕",
    "m3": "📍 **KDE NÁS NAJDETE?**\n\n"
          "🏠 Vyskočilova 1100/2, Praha 4\n"
          "🗺️ Mapa: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
          "Stylová kavárna, příjemná atmosféra – zastavte se!",
    "m4": "📞 **KONTAKTUJTE NÁS**\n\n"
          "📬 E-mail: info@coffeeperk.cz\n"
          "📞 Telefon: +420 725 422 518\n\n"
          "Rezervace, dotazy, doporučení. Jsme tu pro vás!",
    "m5": "📦 **PŘEDOBJEDNÁVKY**\n\n"
          "Brzy spustíme možnost předobjednat si kávu a snídaně přes Telegram.\n"
          "Zatím nás navštivte osobně – těšíme se! ☕️",
    "m6": "😎 **DŮVODY, PROČ SI ZAJÍT NA KÁVU**\n\n"
          "☕ Protože svět se lépe řeší s kofeinem.\n"
          "📚 Protože práce počká – espresso ne.\n"
          "💬 Protože dobrá konverzace začíná u šálku.\n"
          "🧠 Protože mozek startuje až po druhé kávě.\n"
          "🌦️ Protože venku prší... nebo je hezky... prostě čas na kafe.\n\n"
          "Někdy stačí jen důvod k úsměvu. 💛"
}

EN_TEXT = {
    "e1": "**COFFEE PERK MENU ☕️**\n\n"
          "It’s not just coffee here. It’s a little ritual. It’s a mood. It’s... love in a cup. 💘\n\n"
          "☕ Specialty coffee\n"
          "🍳 Breakfast (light & hearty)\n"
          "🍰 Homemade cakes\n"
          "🥗 Brunch & salads\n\n"
          "📄 Full menu:\n"
          "👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
          "Whether it’s espresso, matcha or ginger latte – it just tastes better here. 💛",
    "e2": "**OPENING HOURS 🕐**\n\n"
          "📅 Mon–Fri: 7:30 – 17:00\n"
          "📅 Sat & Sun: CLOSED\n\n"
          "Join us any weekday morning for your coffee fix.",
    "e3": "**FIND US 📍**\n\n"
          "🏠 Vyskočilova 1100/2, Prague 4\n"
          "🗺️ Map: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
          "Cozy spot, great vibes – stop by!",
    "e4": "**CONTACT / BOOKING 📞**\n\n"
          "📬 Email: info@coffeeperk.cz\n"
          "📞 Phone: +420 725 422 518\n\n"
          "Questions, reservations, advice – we’re here!",
    "e5": "**PRE-ORDER SOON 📦**\n\n"
          "Telegram pre-order coming soon – grab your coffee & breakfast ahead!\n"
          "Stay tuned.",
    "e6": "**WHY COFFEE? 😎**\n\n"
          "☕ Because the world runs better on caffeine.\n"
          "📚 Because work can wait – espresso can’t.\n"
          "💬 Because every good chat starts with a cup.\n"
          "🧠 Because brains fire up after round two.\n"
          "🌦️ Because whether rain or shine, it’s coffee time.\n\n"
          "Sometimes the best reason is just to smile. 💛"
}


def section(update, context):
    """Zobrazí konkrétní sekci podle callback_data."""
    key = update.callback_query.data
    update.callback_query.answer()
    if key in CS_TEXT:
        update.callback_query.edit_message_text(CS_TEXT[key], parse_mode="Markdown")
    elif key in EN_TEXT:
        update.callback_query.edit_message_text(EN_TEXT[key], parse_mode="Markdown")


# ─── ZÁPIS HANDLERŮ ────────────────────────────────────────────────────────────

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(menu_cs, pattern="^lang_cs$"))
dp.add_handler(CallbackQueryHandler(menu_en, pattern="^lang_en$"))
dp.add_handler(CallbackQueryHandler(section, pattern="^(m|e)[1-6]$"))


# ─── WEBHOOK ENDPOINT ─────────────────────────────────────────────────────────

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "OK"


@app.route("/")
def index():
    return "Coffee Perk bot is alive ✔️"


if __name__ == "__main__":
    # při startu nastavíme webhook
    bot.set_webhook(f"{BASE_URL}/{TOKEN}")
    # Flask na portu (Render automaticky => $PORT)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
