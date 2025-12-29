import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# ================= CONFIG =================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")
LINKS_FILE = "links.json"
USERS_FILE = "users.json"
# ==========================================

# ---------- JSON HELPERS ----------
def load_json(file, default):
    try:
        with open(file, "r") as f:
            data = json.load(f)
            return data
    except:
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    # Save user
    users = load_json(USERS_FILE, [])
    if not isinstance(users, list):
        users = []
    if user_id not in users:
        users.append(user_id)
        save_json(USERS_FILE, users)

    # Load links
    links = load_json(LINKS_FILE, [])
    text = f"👋 *Hello {first_name}!* 👋\n\n📌 *Important Links:*\n"
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

# ---------- /setlinks (OWNER ONLY) ----------
async def setlinks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Only owner can use this command.")

    context.user_data["set_links_mode"] = True
    await update.message.reply_text(
        "🔗 Send links (one per line).\nThey will be saved automatically."
    )

async def receive_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("set_links_mode"):
        return

    links = [line.strip() for line in update.message.text.splitlines() if line.strip()]
    save_json(LINKS_FILE, links)

    context.user_data["set_links_mode"] = False
    await update.message.reply_text(f"✅ {len(links)} links saved successfully.")

# ---------- /broadcast (OWNER ONLY) ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Only owner can use this command.")

    if not context.args:
        return await update.message.reply_text(
            "Usage:\n/broadcast Your message here"
        )

    message = " ".join(context.args)
    users = load_json(USERS_FILE, [])
    if not isinstance(users, list):
        users = []

    sent = 0
    failed = 0
    for uid in users:
        try:
            await context.bot.send_message(uid, message)
            sent += 1
        except:
            failed += 1

    await update.message.reply_text(f"✅ Broadcast sent to {sent} users.\n❌ Failed: {failed}")

# ---------- MAIN ----------
def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set in environment variables!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setlinks", setlinks))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_links))

    print("🤖 Bot Started (PTB 21.6)")

    # Run polling safely (PTB handles asyncio internally)
    app.run_polling()

if __name__ == "__main__":
    main()
