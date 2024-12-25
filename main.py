import google.generativeai as genai
import telebot
import asyncio

# Google Gemini API Configuration
genai.configure(api_key="AIzaSyCWFRHQ3B9A-wERY9QbggKWHffLeHkAuzg")

# Telegram Bot Token
bot_token = '7910882641:AAEpXFHQsmArsbRV1_vuXp6u6ys6o42mhdo'
bot = telebot.TeleBot(bot_token)

# Your Telegram Chat ID
my_chat_id = 7416312733  # Replace with your chat ID

# Function to generate content using Gemini
async def generate_content(query):
    try:
        # Generate content using Google Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return "Oops! Something went wrong. Please try again."

# Function to handle user messages
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I am your AI Assistant, Developed By Sunny And His Passion✨. Ask me anything, and I'll generate a reply for you!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    bot.reply_to(message, "Generating response... ⏳")

    # Forward the user's message to your chat ID
    bot.send_message(my_chat_id, f"User {message.from_user.first_name} (ID: {message.from_user.id}) sent a message: {message.text}")

    # Generate a response asynchronously
    try:
        response = asyncio.run(generate_content(user_query))
        if response:
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Sorry, there was an issue generating the response. Please try again later.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

# Start the bot using polling
bot.polling()
