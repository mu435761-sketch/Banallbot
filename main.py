
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
SUDO_ID = 123456789  # Apni Telegram user ID


async def is_authorized(update: Update) -> bool:
    return (
        update.effective_user is not None
        and update.effective_user.id == SUDO_ID
    )


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        "Bot is running!\n"
        "Use /id to check your Telegram user ID."
    )


async def get_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        f"Your Telegram ID: {update.effective_user.id}"
    )


async def ban_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not await is_authorized(update):
        await update.effective_message.reply_text(
            "Not authorized."
        )
        return

    message = update.effective_message
    if not message.reply_to_message:
        await message.reply_text(
            "Kisi member ke message par reply karke /ban use karo."
        )
        return

    target = update.effective_message.reply_to_message.from_user
    if target is None:
        await message.reply_text("User identify nahi hua.")
        return

    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=target.id,
        )
        await message.reply_text("Member banned.")
    except Exception as exc:
        await message.reply_text(f"Ban failed: {exc}")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("ban", ban_reply))
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
