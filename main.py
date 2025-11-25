import os
import logging

from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ------------ Logging ------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ------------ Env vars ------------
load_dotenv()  # local .env ke liye, Railway pe env vars se kaam ho jayega

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Recommended fast model:
# docs abhi "gemini-2.5-flash" ko default suggest karte hain
GEMINI_MODEL = "gemini-2.5-flash"  # agar future me naam change ho to docs se update kar lena


# ------------ Gemini client ------------
def get_gemini_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY environment variable set nahi hai.")
    # Gemini Developer API ke liye simple client
    client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def call_gemini(user_message: str) -> str:
    """
    User ka message Gemini ko bhejta hai aur text reply return karta hai.
    """
    client = get_gemini_client()

    prompt = (
        "Tum ek Telegram bot ho jo user ko friendly tariqe se answer karta hai. "
        "Reply short, clear Hinglish (Hindi + simple English mix) me karo. "
        "User message: " + user_message
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
    except Exception as e:
        logger.exception("Gemini API request fail hua: %s", e)
        return "Gemini API se connect nahi ho pa raha 😅. Thodi der baad try karo."

    # Normal case – response.text me final output hota hai
    try:
        text = getattr(response, "text", None)
        if not text:
            # Kabhi-kabhi candidates/parts ke andar bhi ho sakta hai
            candidates = getattr(response, "candidates", None) or []
            if candidates and hasattr(candidates[0], "content"):
                parts = getattr(candidates[0].content, "parts", None) or []
                if parts and hasattr(parts[0], "text"):
                    text = parts[0].text

        if not text:
            logger.error("Gemini response me text nahi mila: %s", response)
            return "Gemini se ajeeb response aaya 😅. Thodi der baad try karo."
        return text
    except Exception:
        logger.exception("Gemini response parse karte waqt error.")
        return "Gemini ka reply parse nahi ho paya 😅."


# ------------ Telegram handlers ------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Namaste! 👋\n\n"
        "Main Gemini powered Telegram bot hoon.\n"
        "Jo bhi sawaal hai, yahan bhejo 🙂"
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "/start – bot shuru karo\n"
        "Bas normal message bhejo, main Gemini se reply launga."
    )
    await update.message.reply_text(text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    user_id = update.effective_user.id if update.effective_user else None

    logger.info("User %s: %s", user_id, user_text)

    try:
        reply_text = call_gemini(user_text)
    except Exception:
        logger.exception("Unexpected error in call_gemini()")
        reply_text = (
            "Backend me kuch error aa gaya 😅\n"
            "Thodi der baad dobara try kar lena."
        )

    await update.message.reply_text(reply_text)


# ------------ Main (no asyncio.run) ------------

def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable set nahi hai.")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Gemini Telegram bot started (run_polling)...")
    application.run_polling()


if __name__ == "__main__":
    main()
