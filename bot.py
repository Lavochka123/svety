# bot.py
import logging
import qrcode
from urllib.parse import quote
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CallbackContext
)

# Стадии диалога
DESIGN, INTRO, PROPOSAL, TIMES = range(4)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Настоящее свидание начинается с красивого приглашения. Давай сделаем его идеальным!\n\n"
        "Выбери дизайн для открытки:"
    )
    keyboard = [
        [InlineKeyboardButton("🎆 Элегантная ночь", callback_data="design_elegant")],
        [InlineKeyboardButton("🌹 Романтика", callback_data="design_romantic")],
        [InlineKeyboardButton("🎶 Музыка и кино", callback_data="design_music")],
        [InlineKeyboardButton("💡 Минимализм", callback_data="design_minimal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери один из вариантов:", reply_markup=reply_markup)
    return DESIGN

async def design_choice(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    design = query.data
    context.user_data["design"] = design
    await query.edit_message_text(
        text=f"Ты выбрал {design}. Введи вступительный текст для приглашения:"
    )
    return INTRO

async def get_intro(update: Update, context: CallbackContext) -> int:
    intro_text = update.message.text
    context.user_data["intro"] = intro_text
    await update.message.reply_text("Теперь напиши само предложение для встречи:")
    return PROPOSAL

async def get_proposal(update: Update, context: CallbackContext) -> int:
    proposal_text = update.message.text
    context.user_data["proposal"] = proposal_text
    await update.message.reply_text(
        "Укажи 3 варианта времени для встречи (например, в формате:\n"
        "🕗 19:00 | 21 января\n"
        "🌙 20:30 | 22 января\n"
        "☕ 17:00 | 23 января)"
    )
    return TIMES

async def get_times(update: Update, context: CallbackContext) -> int:
    times_text = update.message.text
    context.user_data["times"] = times_text.splitlines()  # разбиваем варианты по строкам

    # Получаем сохранённые данные
    design = context.user_data.get("design", "design_elegant")
    intro = context.user_data.get("intro", "Привет! Я подготовил для тебя нечто особенное...")
    proposal = context.user_data.get("proposal", "Давай проведём этот вечер вместе. Я знаю уютное место!")
    times = context.user_data.get("times", ["🕗 19:00 | 21 января", "🌙 20:30 | 22 января", "☕ 17:00 | 23 января"])

    # Кодируем строки для URL
    encoded_intro = quote(intro)
    encoded_proposal = quote(proposal)

    # Получаем chat_id текущего чата
    chat_id = update.effective_chat.id

    # Формируем URL для приглашения (предполагается, что Flask-сервер запущен на http://127.0.0.1:5000)
    invite_url = (f"http://127.0.0.1:5000/invite/unique_invite_id?"
                  f"design={design}&intro={encoded_intro}&proposal={encoded_proposal}"
                  f"&chat_id={chat_id}")

    # Генерация QR‑кода (опционально)
    img = qrcode.make(invite_url)
    img_path = "invite_qr.png"
    img.save(img_path)

    await update.message.reply_text(
        f"Отлично! Мини‑сайт готов. Открой этот URL в браузере для просмотра приглашения:\n{invite_url}"
    )
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token("ВАШ_ТОКЕН_БОТА").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            DESIGN: [CallbackQueryHandler(design_choice)],
            INTRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_intro)],
            PROPOSAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_proposal)],
            TIMES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_times)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
# bot.py
import logging
import qrcode
from urllib.parse import quote
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CallbackContext
)

# Стадии диалога
DESIGN, INTRO, PROPOSAL, TIMES = range(4)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Настоящее свидание начинается с красивого приглашения. Давай сделаем его идеальным!\n\n"
        "Выбери дизайн для открытки:"
    )
    keyboard = [
        [InlineKeyboardButton("🎆 Элегантная ночь", callback_data="design_elegant")],
        [InlineKeyboardButton("🌹 Романтика", callback_data="design_romantic")],
        [InlineKeyboardButton("🎶 Музыка и кино", callback_data="design_music")],
        [InlineKeyboardButton("💡 Минимализм", callback_data="design_minimal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери один из вариантов:", reply_markup=reply_markup)
    return DESIGN

async def design_choice(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    design = query.data
    context.user_data["design"] = design
    await query.edit_message_text(
        text=f"Ты выбрал {design}. Введи вступительный текст для приглашения:"
    )
    return INTRO

async def get_intro(update: Update, context: CallbackContext) -> int:
    intro_text = update.message.text
    context.user_data["intro"] = intro_text
    await update.message.reply_text("Теперь напиши само предложение для встречи:")
    return PROPOSAL

async def get_proposal(update: Update, context: CallbackContext) -> int:
    proposal_text = update.message.text
    context.user_data["proposal"] = proposal_text
    await update.message.reply_text(
        "Укажи 3 варианта времени для встречи (например, в формате:\n"
        "🕗 19:00 | 21 января\n"
        "🌙 20:30 | 22 января\n"
        "☕ 17:00 | 23 января)"
    )
    return TIMES

async def get_times(update: Update, context: CallbackContext) -> int:
    times_text = update.message.text
    context.user_data["times"] = times_text.splitlines()  # разбиваем варианты по строкам

    # Получаем сохранённые данные
    design = context.user_data.get("design", "design_elegant")
    intro = context.user_data.get("intro", "Привет! Я подготовил для тебя нечто особенное...")
    proposal = context.user_data.get("proposal", "Давай проведём этот вечер вместе. Я знаю уютное место!")
    times = context.user_data.get("times", ["🕗 19:00 | 21 января", "🌙 20:30 | 22 января", "☕ 17:00 | 23 января"])

    # Кодируем строки для URL
    encoded_intro = quote(intro)
    encoded_proposal = quote(proposal)

    # Получаем chat_id текущего чата
    chat_id = update.effective_chat.id

    # Формируем URL для приглашения (предполагается, что Flask-сервер запущен на http://127.0.0.1:5000)
    invite_url = (f"http://127.0.0.1:5000/invite/unique_invite_id?"
                  f"design={design}&intro={encoded_intro}&proposal={encoded_proposal}"
                  f"&chat_id={chat_id}")

    # Генерация QR‑кода (опционально)
    img = qrcode.make(invite_url)
    img_path = "invite_qr.png"
    img.save(img_path)

    await update.message.reply_text(
        f"Отлично! Мини‑сайт готов. Открой этот URL в браузере для просмотра приглашения:\n{invite_url}"
    )
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token("ВАШ_ТОКЕН_БОТА").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            DESIGN: [CallbackQueryHandler(design_choice)],
            INTRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_intro)],
            PROPOSAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_proposal)],
            TIMES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_times)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
