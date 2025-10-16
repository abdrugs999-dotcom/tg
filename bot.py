import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MUST_JOIN_CHANNEL = os.getenv("MUST_JOIN_CHANNEL")
WITHDRAW_CHANNEL_ID = os.getenv("WITHDRAW_CHANNEL_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Must-join channel check
    try:
        member = await context.bot.get_chat_member(MUST_JOIN_CHANNEL, user.id)
        if member.status in ["left", "kicked"]:
            await update.message.reply_text(
                f"❌ প্রথমে আমাদের চ্যানেলে জয়েন করুন: {MUST_JOIN_CHANNEL}\n\nতারপর আবার /start দিন।"
            )
            return
    except Exception:
        await update.message.reply_text(
            f"⚠️ প্রথমে আমাদের চ্যানেলে জয়েন করুন: {MUST_JOIN_CHANNEL}\n\nতারপর আবার চেষ্টা করুন।"
        )
        return

    await update.message.reply_text(f"Assalamu alaikum {user.first_name}! ✅ আপনি সফলভাবে চ্যানেলে যুক্ত হয়েছেন।")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /withdraw <amount>")
        return

    amount = args[0]
    user = update.effective_user
    msg = (
        f"💸 New withdraw request!\n\n"
        f"👤 User: {user.mention_html()}\n"
        f"💰 Amount: {amount}"
    )
    await context.bot.send_message(chat_id=WITHDRAW_CHANNEL_ID, text=msg, parse_mode="HTML")
    await update.message.reply_text("✅ আপনার উইথড্র রিকোয়েস্ট পাঠানো হয়েছে।")

def main():
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN সেট করা হয়নি! অনুগ্রহ করে .env ফাইল চেক করুন।")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.run_polling()

if __name__ == "__main__":
    main()
