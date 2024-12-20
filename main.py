

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import google.generativeai as genai

# Telegram and Gemini API keys
TELEGRAM_TOKEN = ""
GEMINI_API_KEY = "
# Initialize the Telegram Bot and Dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate a more explicit adult response in Hinglish
def generate_adult_response(user_input):
    try:
        response = model.generate_content(f"Respond like a real erotic girlfriend, always first you msg, but too much loving, little talk, supportive, and loving and say everything in Hinglish. The user said: {user_input}")
        return response.text.strip()
    except Exception as e:
        return f"Sorry baby, I can't fulfill that request right now. 😘"

# Start Command: Start conversation with the bot
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Hi there! 💕 I'm your girlfriend bby! 💖 How can I make your day better? 😊")

# Default Message Handler: Respond to user input with adult Hinglish response
@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    response = generate_adult_response(user_input)
    await message.reply(response)

# Run the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
