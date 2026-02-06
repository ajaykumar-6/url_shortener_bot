import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SHORTIO_API_KEY = os.getenv("SHORTIO_API_KEY")
SHORTIO_DOMAIN = os.getenv("SHORTIO_DOMAIN")  # example: yourdomain.short.gy

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send me any long URL and I’ll shorten it using Short.io 🔗"
    )

# URL handler
async def shorten_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    long_url = update.message.text.strip()

    payload = {
        "originalURL": long_url,
        "domain": SHORTIO_DOMAIN,
    }

    headers = {
        "Authorization": SHORTIO_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            "https://api.short.io/links",
            json=payload,
            headers=headers,
            timeout=10,
        )

        if response.status_code == 200 or response.status_code == 201:
            short_url = response.json().get("shortURL")
            await update.message.reply_text(f"✅ Shortened URL:\n{short_url}")
        else:
            await update.message.reply_text(
                "❌ Failed to shorten the URL. Please try again."
            )

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Something went wrong. Try later.")

# Main entry point
def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, shorten_url))

    application.run_polling()

if __name__ == "__main__":
    main()
