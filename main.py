import google.generativeai as genai
import telebot
import asyncio

# Google Gemini API Configuration
genai.configure(api_key="AIzaSyCWFRHQ3B9A-wERY9QbggKWHffLeHkAuzg")
model = genai.GenerativeModel("gemini-1.5-flash")

# Telegram Bot Token
bot_token = '7910882641:AAEpXFHQsmArsbRV1_vuXp6u6ys6o42mhdo'
bot = telebot.TeleBot(bot_token)

# Function to generate ethical hacking scripts
async def generate_script(query):
    response = model.generate_content(query)
    return response.text

# Function to handle user messages
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your Ethical Hacking Assistant. Send me a query, and I'll generate a script for you!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    bot.reply_to(message, "Generating script, please wait... ⏳")

    # Generate script asynchronously
    response = asyncio.run(generate_script(user_query))

    # Send the generated script to the user
    bot.reply_to(message, f"Here is your generated script:\n{response}")

# Start the bot using polling
bot.polling()
