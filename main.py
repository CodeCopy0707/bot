import google.generativeai as genai
import telebot
import asyncio

# Google Gemini API Configuration
genai.configure(api_key="AIzaSyCWFRHQ3B9A-wERY9QbggKWHffLeHkAuzg")

# Telegram Bot Token
bot_token = '7910882641:AAEpXFHQsmArsbRV1_vuXp6u6ys6o42mhdo'
bot = telebot.TeleBot(bot_token)

# Function to generate creative and fun replies using Google Gemini
async def generate_fun_reply(query):
    try:
        response = genai.generate_text(query)
        return response.text
    except Exception as e:
        print(f"Error generating reply: {str(e)}")
        return "Oops! Something went wrong. Let me try again. 😅"

# Function to handle user messages
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your fun assistant 🤖✨. Ask me anything, and I'll generate a fun reply for you!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    bot.reply_to(message, "Generating fun reply... ⏳")

    # Generate a fun reply asynchronously using Google Gemini
    try:
        response = asyncio.run(generate_fun_reply(user_query))
        if response:
            # Send the generated fun reply to the user
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Sorry, there was an issue generating the reply. Please try again later.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

# Start the bot using polling
bot.polling()
