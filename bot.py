import json
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# ========== CONFIG ==========
BOT_TOKEN = "7730773830:AAFAMDT5w_wbrTcv2tl8YwbV6rfzY0CYfHI"
CHANNEL_USERNAME = "biomute_bot"  # without @

LINKS_FILE = "links.json"
USERS_FILE = "users.json"
# ============================


# ---------- JSON HELPERS ----------
def load_json(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return default


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Save user safely
    users = load_json(USERS_FILE, [])
    if not isinstance(users, list):
        users = []

    if user_id not in users:
        users.append(user_id)
        save_json(USERS_FILE, users)

    # Load links safely
    links = load_json(LINKS_FILE, [])
    if not isinstance(links, list):
        links = []

    text = "👋 *Welcome!*\n\n📌 *Important Links:*\n\n"
    if links:
        for i, link in enumerate(links, 1):
            text += f"{i}. {link}\n"
    else:
        text += "_No links set yet._"

    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# ---------- /setlinks ----------
async def setlinks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["set_links_mode"] = True
    await update.message.reply_text(
        "🔗 Links bhejo (har line me ek link).\n\nSend karte hi save ho jayenge."
    )


async def receive_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("set_links_mode"):
        return

    links = [line.strip() for line in update.message.text.splitlines() if line.strip()]
    save_json(LINKS_FILE, links)

    context.user_data["set_links_mode"] = False
    await update.message.reply_text(f"✅ {len(links)} links save ho gaye.")


# ---------- /broadcast ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text(
            "Usage:\n/broadcast Your message here"
        )

    message = " ".join(context.args)
    users = load_json(USERS_FILE, [])
    if not isinstance(users, list):
        users = []

    sent = 0
    for uid in users:
        try:
            await context.bot.send_message(uid, message)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"✅ Broadcast sent to {sent} users.")


# ---------- MAIN ----------
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setlinks", setlinks))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_links))

    print("🤖 Bot Started (PTB 21+ on Heroku)")
    await app.run_polling()


if __name__ == "__main__":
    # ✅ Heroku / PTB 21+ loop fix
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(main())
