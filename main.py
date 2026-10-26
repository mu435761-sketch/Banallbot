import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Yahan apna BotFather se mila Token paste karo (Quotes ke andar)
TOKEN = "8885117959:AAGlPm6ncqDU5gTqFC0ElvPXJQZf_fqfINQ"

# 2. Yahan apni Telegram ID daalo (Number ke saath)
SUDO_ID = 5029489287  # Apni ID yahan daalo

async def ban_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SUDO_ID:
        await update.message.reply_text("❌ You are not authorized!")
        return

    chat_id = update.effective_chat.id
    await update.message.reply_text("🚫 Banning all members...")

    try:
        members = await context.bot.get_chat_members(chat_id)
        count = 0
        for member in members:
            if member.user.is_bot or member.status == 'administrator':
                continue
            try:
                await context.bot.ban_chat_member(chat_id, member.user.id)
                count += 1
                await asyncio.sleep(0.5) 
            except Exception:
                pass
        
        await update.message.reply_text(f"✅ Successfully banned {count} members.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Use /banall to ban all users.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("banall", ban_all))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
