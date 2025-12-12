from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os

TOKEN = os.getenv("8561347115:AAH7Pf59Llqrv9upyjVF7hc6biG1NsCYrko")  # Railway env variable


# ---------------------------
# START COMMAND (HOME MENU)
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🔍 Scan My Number", callback_data="scan")],
        [InlineKeyboardButton("🧹 Remove My Data", callback_data="remove")],
        [InlineKeyboardButton("📝 Auto Removal Message", callback_data="auto_msg")],
        [InlineKeyboardButton("🛡 Privacy Tips", callback_data="tips")]
    ]

    await update.message.reply_text(
        "🔐 *Welcome to PrivacyGuardBot (Safe Version)*\n\n"
        "Ye bot aapka number public websites par dikh raha hai ya nahi,\n"
        "uske baare me basic visibility info deta hai.\n\n"
        "⚠️ *Note:* Bot koi personal data store nahi karta.\n\n"
        "Choose an option 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------------------
# INLINE BUTTON HANDLER
# ---------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "scan":
        await query.message.reply_text(
            "Please enter *your own* phone number:\nExample: +91XXXXXXXXXX",
            parse_mode="Markdown"
        )

    elif query.data == "remove":
        await send_removal_menu(query)

    elif query.data == "auto_msg":
        await send_auto_message(query)

    elif query.data == "tips":
        await send_privacy_tips(query)


# ---------------------------
# HANDLE PHONE NUMBER
# ---------------------------
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()

    if not number.startswith("+"):
        await update.message.reply_text("❌ Please enter number like +91XXXXXXXXXX")
        return

    await update.message.reply_text("🔎 Scanning public directories…")

    google_link = f"https://www.google.com/search?q={number}+owner"
    directory_link = f"https://www.example.com/phone/{number}"

    report = (
        "📊 *Privacy Exposure Report*\n"
        "———————————————\n\n"
        f"🔍 Google Search Visibility:\n{google_link}\n\n"
        f"📱 Public Caller Directory:\n{directory_link}\n\n"
        "———————————————\n"
        "🧹 Use buttons below to remove public data."
    )

    keyboard = [
        [InlineKeyboardButton("🧹 Remove From Truecaller", url="https://www.truecaller.com/unlisting")],
        [InlineKeyboardButton("🧹 Remove From Caller Directory", url=directory_link)],
        [InlineKeyboardButton("📝 Auto Removal Message", callback_data="auto_msg")]
    ]

    await update.message.reply_text(report, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


# ---------------------------
# REMOVAL MENU
# ---------------------------
async def send_removal_menu(query):
    keyboard = [
        [InlineKeyboardButton("Truecaller Unlist", url="https://www.truecaller.com/unlisting")],
        [InlineKeyboardButton("Google Removal Tool", url="https://support.google.com/websearch/troubleshooter/3111061")],
        [InlineKeyboardButton("Auto Removal Message", callback_data="auto_msg")],
    ]

    await query.message.reply_text(
        "🧹 *Data Removal Center*\n\nSelect a platform to request removal:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------------------
# AUTO-FILL MESSAGE
# ---------------------------
async def send_auto_message(query):
    msg = (
        "📄 *Auto-Filled Removal Message:*\n\n"
        "“This number belongs to me. Please remove all publicly visible data "
        "due to privacy and safety concerns.”\n\n"
        "Copy this message on any website’s removal form."
    )
    await query.message.reply_text(msg, parse_mode="Markdown")


# ---------------------------
# PRIVACY TIPS
# ---------------------------
async def send_privacy_tips(query):
    tips = (
        "🛡 *Privacy Tips*\n\n"
        "• Unknown apps ko Contacts access mat do\n"
        "• Telegram bots me personal info mat daalo\n"
        "• Public groups me number mat share karo\n"
        "• SIM KYC updated rakho\n"
        "• Regular privacy scan karo\n"
    )
    await query.message.reply_text(tips, parse_mode="Markdown")


# ---------------------------
# MAIN BOT
# ---------------------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))

print("🚀 Bot Running on Railway…")
app.run_polling()
