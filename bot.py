import requests
from PIL import Image
from io import BytesIO
import telebot
import openai
import g4f
import time
from datetime import datetime, timedelta

# Replace with your actual bot token and OpenAI API key
TOKEN = "8145529781:AAF0FsG70As3EoL995Wq3z6nIoTDnQOLIs4"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

# Function to generate AI images
def generate_ai_image(prompt):
    response = g4f.ImageGeneration.create(
        model="dalle",  # or use "stable-diffusion"
        prompt=prompt
    )
    return response  # Returns the image URL

# Handle image requests
@bot.message_handler(commands=['image'])
def send_ai_image(message):
    user_prompt = message.text.replace("/image", "").strip()
    if not user_prompt:
        bot.reply_to(message, "Please provide a description. Example: /image a futuristic city")
        return

    bot.reply_to(message, "Generating image... Please wait.")
    
    image_url = generate_ai_image(user_prompt)
    
    if image_url:
        bot.send_photo(message.chat.id, image_url, caption="Here is your AI-generated image! 🎨")
    else:
        bot.reply_to(message, "Sorry, I couldn't generate the image. Try again!")

# AI Chat Function
def get_ai_response(user_input):
    response = g4f.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5"
        messages=[{"role": "user", "content": user_input}]
    )
    return response

# Handle all text messages with AI
@bot.message_handler(func=lambda message: True)
def ai_chat(message):
    user_text = message.text
    ai_response = get_ai_response(user_text)
    bot.reply_to(message, ai_response)

# Welcome new members
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        welcome_text = f"🎉 Welcome, {new_member.first_name}! 🎉\n\nGlad to have you in this group. Feel free to ask questions and engage! Please read the rules below:"
        rules_text = """
📌 **Group Rules** 📌  
1️⃣ Be respectful to everyone.  
2️⃣ No spamming or self-promotion.  
3️⃣ Stay on topic and avoid off-topic discussions.  
4️⃣ No hate speech or offensive content.  
5️⃣ Follow all Telegram guidelines.  

Enjoy your stay! 🚀
"""

        bot.send_message(message.chat.id, welcome_text)
        bot.send_message(message.chat.id, rules_text)

# Ban command to remove a user
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:  # Check if the command is used as a reply
        user_id = message.reply_to_message.from_user.id
        try:
            bot.kick_chat_member(message.chat.id, user_id)
            bot.send_message(message.chat.id, f"User {message.reply_to_message.from_user.first_name} has been removed.\nNice knowing you! 😊")
        except Exception as e:
            bot.reply_to(message, f"Error: {str(e)}")
    else:
        bot.reply_to(message, "Reply to a user's message with /ban to remove them.")

# Start bot
print("AI Chat Bot is Running...")
bot.polling()
