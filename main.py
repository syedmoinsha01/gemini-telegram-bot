import os
import logging
import asyncio

from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.constants import ChatAction
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
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"

# ------------ Memory Store (per user) ------------
# Structure:
# user_memory[user_id] = [{"role": "user/assistant", "content": "..."}]
user_memory = {}
MEMORY_LIMIT = 20  # max messages to keep per user


# ------------ Gemini client ------------
def get_gemini_client() -> genai.Client:
    client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def call_gemini_with_memory(user_id: int, user_message: str) -> str:
    """
    Send chat history + new message to Gemini.
    """

    # Ek user ki memory fetch karo
    history = user_memory.get(user_id, [])

    # New user message ko history me add karo
    history.append({"role": "user", "content": user_message})

    # Agar memory bahut zyada ho gayi ho, purane messages hata do
    if len(history) > MEMORY_LIMIT:
        history = history[-MEMORY_LIMIT:]

    # Gemini prompt format
    formatted_messages = []
    for msg in history:
        formatted_messages.append(f"{msg['role']}: {msg['content']}")

    final_prompt = "\n".join(formatted_messages)

    client = get_gemini_client()

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=final_prompt,
        )
    except Exception as e:
        logger.exception("Gemini API fail: %s", e)
        return "Gemini API se connect nahi ho pa raha 😅. Thodi der baad try karo."

    # Response extract
    try:
        reply = response.text
    except:
        reply = "Gemini ka reply parse nahi ho paya 😅."

    # Assistant ka reply memory me store karo
    history.append({"role": "assistant", "content": reply})

    # Again limit enforce
    if len(history) > MEMORY_LIMIT:
        history = history[-MEMORY_LIMIT:]

    # Save memory back
    user_memory[user_id] = history

    return reply


# ------------ Telegram handlers ------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Namaste! 👋\n\nMain Gemini powered bot hoon.\n"
        "Main ab tumhari chat *yaad rakhunga* 🧠🙂"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/start – bot shuru karo\n"
        "/forget – apni chat memory reset karo\n"
        "Normal message bhejo, main answer dunga."
    )


async def forget_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_memory[user_id] = []
    await update.message.reply_text("Theek hai! Maine tumhari puri memory reset kar di 🤝")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    user_id = update.effective_user.id

    logger.info("User %s: %s", user_id, user_text)

    # Show typing…
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
    except:
        pass

    # Call Gemini in background thread
    reply_text = await asyncio.to_thread(
        call_gemini_with_memory, user_id, user_text
    )

    await update.message.reply_text(reply_text)


# ------------ Main ------------

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("forget", forget_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Gemini bot (with memory) started...")
    application.run_polling()


if __name__ == "__main__":
    main()
