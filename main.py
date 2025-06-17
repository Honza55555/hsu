import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

TOKEN    = os.environ['TELEGRAM_TOKEN']
BASE_URL = os.environ['BASE_URL']  # nastavte např. https://vaše-služba.onrender.com

bot        = Bot(token=TOKEN)
app        = Flask(__name__)
dispatcher = Dispatcher(bot, update_queue=None, workers=0, use_context=True)

# ————— HANDLERY —————

def start(update, context):
    kb = [
        [
            InlineKeyboardButton("🇨🇿 Čeština", callback_data='lang:cz'),
            InlineKeyboardButton("🌍 English", callback_data='lang:en')
        ]
    ]
    update.message.reply_text(
        "☕️ Vítejte v Coffee Perk!\nWe’re happy to see you here. 🌟\nPlease choose your language. 🗣️",
        reply_markup=InlineKeyboardMarkup(kb)
    )

def menu_cz(update, context):
    kb = [
        [InlineKeyboardButton("🧾 Menu a nabídka",      callback_data='cz:menu')],
        [InlineKeyboardButton("🕐 Otevírací doba",      callback_data='cz:hours')],
        [InlineKeyboardButton("📍 Kde nás najdete",     callback_data='cz:where')],
        [InlineKeyboardButton("📞 Kontakt / Rezervace", callback_data='cz:contact')],
        [InlineKeyboardButton("📦 Předobjednávka",      callback_data='cz:preorder')],
        [InlineKeyboardButton("😎 Proč k nám na kávu?", callback_data='cz:why')],
    ]
    update.callback_query.edit_message_text(
        "Na co se mě můžeš zeptat:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

def menu_en(update, context):
    kb = [
        [InlineKeyboardButton("🧾 Menu & Offerings",    callback_data='en:menu')],
        [InlineKeyboardButton("🕐 Opening Hours",       callback_data='en:hours')],
        [InlineKeyboardButton("📍 Find Us",             callback_data='en:where')],
        [InlineKeyboardButton("📞 Contact / Booking",   callback_data='en:contact')],
        [InlineKeyboardButton("📦 Pre-order (soon)",     callback_data='en:preorder')],
        [InlineKeyboardButton("😎 Why Coffee Perk?",     callback_data='en:why')],
    ]
    update.callback_query.edit_message_text(
        "What can I help you with?",
        reply_markup=InlineKeyboardMarkup(kb)
    )

# ——— ČESKÉ SEKCE ———

CZ = {
  'menu': """🥐 COFFEE PERK MENU ☕️
U nás nejde jen o kafe. Je to malý rituál. Je to nálada. Je to... láska v šálku. 💘

☕ Výběrová káva
🍳 Snídaně (lehké i pořádné)
🍰 Domácí dorty
🥗 Brunch a saláty

👉 https://www.coffeeperk.cz/jidelni-listek"""
, 'hours': """🕐 KDY MÁME OTEVŘENO?
📅 Po–Pá: 7:30–17:00
📅 So–Ne: ZAVŘENO"""
, 'where': """📍 KDE NÁS NAJDETE?
🏠 Vyskočilova 1100/2, Praha 4
🗺️ https://goo.gl/maps/XU3nYKDcCmC2"""
, 'contact': """📞 KONTAKTUJTE NÁS
✉️ info@coffeeperk.cz
📱 +420 725 422 518"""
, 'preorder': """📦 PŘEDOBJEDNÁVKY
Brzy spustíme objednávky přes Telegram. Sledujte nás!"""
, 'why': """😎 PROČ SI ZAJÍT NA KÁVU
☕ Svět se lépe řeší s kofeinem.
📚 Práce počká – espresso ne.
💬 Dobrý rozhovor začíná u šálku.
🧠 Mozek běží až po druhé kávě."""
}

# ——— ANGLICKÉ SEKCE ———

EN = {
  'menu': """🥐 COFFEE PERK MENU ☕️
It’s not just coffee. It’s a small ritual. It’s a mood. It’s… love in a cup. 💘

☕ Specialty coffee
🍳 Breakfast
🍰 Homemade cakes
🥗 Brunch & salads

👉 https://www.coffeeperk.cz/jidelni-listek"""
, 'hours': """🕐 OPENING HOURS
📅 Mon–Fri: 7:30–17:00
📅 Sat & Sun: CLOSED"""
, 'where': """📍 FIND US
🏠 Vyskočilova 1100/2, Prague 4
🗺️ https://goo.gl/maps/XU3nYKDcCmC2"""
, 'contact': """📞 CONTACT / BOOKING
✉️ info@coffeeperk.cz
📱 +420 725 422 518"""
, 'preorder': """📦 PRE-ORDER
Pre-ordering via Telegram coming soon. Stay tuned!"""
, 'why': """😎 WHY COFFEE PERK?
☕ The world runs better on caffeine.
📚 Work can wait – espresso can’t.
💬 Great convos start over a cup.
🧠 Brain kicks in after the second cup."""
}

def button_router(update, context):
    data = update.callback_query.data.split(':')
    lang, key = data
    if lang == 'lang':
        if key == 'cz': return menu_cz(update, context)
        else:         return menu_en(update, context)
    text = (CZ if lang=='cz' else EN).get(key, "❓")
    update.callback_query.edit_message_text(text)

# ————— WEBHOOK ENDPOINT —————

@app.route(f"/webhook/{TOKEN}", methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# ————— REGISTRACE HANDLERŮ —————

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(button_router))

if __name__ == "__main__":
    # při spuštění na Renderu zaregistrujeme webhook
    webhook_url = f"{BASE_URL}/webhook/{TOKEN}"
    bot.set_webhook(webhook_url)
    port = int(os.environ.get("PORT", "5000"))
    app.run(host='0.0.0.0', port=port)
