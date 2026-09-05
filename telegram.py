import os

from dotenv import load_dotenv

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)


# =========================
# Load Environment Variables
# =========================

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# =========================
# Conversation States
# =========================

NAME, AGE = range(2)


# =========================
# Reply Keyboard
# =========================

reply_keyboard = ReplyKeyboardMarkup(
    [
        ["📋 منوی اصلی"],
        ["❓ راهنما", "ℹ️ درباره ما"],
    ],
    resize_keyboard=True,
)


# =========================
# Inline Keyboard
# =========================

def main_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "👤 پروفایل",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                "⚙️ تنظیمات",
                callback_data="settings"
            ),
        ],
        [
            InlineKeyboardButton(
                "📦 محصولات",
                callback_data="products"
            ),
        ],
        [
            InlineKeyboardButton(
                "📝 ثبت نام",
                callback_data="register"
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# Start Command
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    await update.message.reply_text(
        f"""
👋 سلام {user.first_name}

به ربات ما خوش آمدی 🤖

از منوی زیر یک گزینه را انتخاب کن:
""",
        reply_markup=reply_keyboard
    )

    await update.message.reply_text(
        "📋 منوی اصلی:",
        reply_markup=main_menu()
    )


# =========================
# Reply Keyboard Handler
# =========================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if text == "📋 منوی اصلی":

        await update.message.reply_text(
            "📋 منوی اصلی:",
            reply_markup=main_menu()
        )

    elif text == "❓ راهنما":

        await update.message.reply_text(
            """
🤖 راهنمای ربات

از دکمه‌های منو استفاده کن.

👤 پروفایل:
مشاهده اطلاعات کاربر

📦 محصولات:
مشاهده محصولات

📝 ثبت نام:
ثبت نام در ربات
"""
        )

    elif text == "ℹ️ درباره ما":

        await update.message.reply_text(
            "این یک پروژه آموزشی با python-telegram-bot است 🚀"
        )


# =========================
# Callback Handler
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    # پاسخ به Callback Query
    await query.answer()

    # داده دکمه
    data = query.data


    # ---------------------
    # Profile
    # ---------------------

    if data == "profile":

        user = update.effective_user

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            text=f"""
👤 پروفایل شما

نام: {user.first_name}
نام کاربری: @{user.username}
شناسه: {user.id}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ---------------------
    # Settings
    # ---------------------

    elif data == "settings":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            text="""
⚙️ تنظیمات

در آینده تنظیمات ربات اینجا قرار می‌گیرد.
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ---------------------
    # Products
    # ---------------------

    elif data == "products":

        keyboard = [
            [
                InlineKeyboardButton(
                    "📱 موبایل",
                    callback_data="mobile"
                ),
                InlineKeyboardButton(
                    "💻 لپ‌تاپ",
                    callback_data="laptop"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            text="📦 دسته‌بندی محصولات:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ---------------------
    # Mobile
    # ---------------------

    elif data == "mobile":

        await query.edit_message_text(
            """
📱 محصولات موبایل

1️⃣ iPhone
2️⃣ Samsung
3️⃣ Xiaomi
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="products"
                        )
                    ]
                ]
            )
        )


    # ---------------------
    # Laptop
    # ---------------------

    elif data == "laptop":

        await query.edit_message_text(
            """
💻 محصولات لپ‌تاپ

1️⃣ ASUS
2️⃣ Lenovo
3️⃣ MacBook
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="products"
                        )
                    ]
                ]
            )
        )


    # ---------------------
    # Back
    # ---------------------

    elif data == "back":

        await query.edit_message_text(
            "📋 منوی اصلی:",
            reply_markup=main_menu()
        )


# =========================
# Start Registration
# =========================

async def register_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "📝 لطفاً نام خود را وارد کنید:"
    )

    return NAME


# =========================
# Get Name
# =========================

async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "🎂 حالا سن خود را وارد کنید:"
    )

    return AGE


# =========================
# Get Age
# =========================

async def get_age(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["age"] = update.message.text

    name = context.user_data["name"]
    age = context.user_data["age"]

    await update.message.reply_text(
        f"""
✅ ثبت نام با موفقیت انجام شد

👤 نام: {name}
🎂 سن: {age}
"""
    )

    return ConversationHandler.END


# =========================
# Cancel Conversation
# =========================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "❌ عملیات لغو شد."
    )

    return ConversationHandler.END


# =========================
# Main
# =========================

def main():

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )


    # ---------------------
    # Conversation Handler
    # ---------------------

    conversation_handler = ConversationHandler(

        entry_points=[
            CallbackQueryHandler(
                register_start,
                pattern="^register$"
            )
        ],

        states={

            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],

            AGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_age
                )
            ],
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel
            )
        ],
    )


    # ---------------------
    # Add Handlers
    # ---------------------

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        conversation_handler
    )

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )


    # ---------------------
    # Run Bot
    # ---------------------

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
