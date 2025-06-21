from extract import the_daily_sun, the_daily_star, the_prothom_alo
from transfer import gemini_response, make_decision, gemini_query
from dotenv import load_dotenv
import os
from telebot import TeleBot
import time
import threading
import json

load_dotenv()

last_context = None
token = os.getenv("token")
CHAT_ID = os.getenv("CHAT_ID")
MONGODB_URI = os.getenv("MONGODB_URI")
bot = TeleBot(token)



def send_message_to_telegram(message):
    bot.send_message(CHAT_ID, message)

def get_news():
    headlines = []
    sun_news = the_daily_sun()
    headlines.extend(gemini_response(sun_news))
    star_news = the_daily_star()
    headlines.extend(gemini_response(star_news))
    prothom_alo_news = the_prothom_alo()
    headlines.extend(gemini_response(prothom_alo_news))

    # Save the news to a json file
    with open("news.json", "w") as f:
        json.dump(headlines, f, indent=4)
    

    full_message = ""
    if sun_news:
        full_message += "The daily sun news added. \n\n"
    else:
        full_message += "The daily sun news not added. \n\n"
    if star_news:
        full_message += "The daily star news added. \n\n"
    else:
        full_message += "The daily star news not added. \n\n"
    if prothom_alo_news:
        full_message += "The prothom alo news added. \n\n"
    else:
        full_message += "The prothom alo news not added. \n\n"

    return full_message 

def start_sending_news():
    while True:
        global last_context
        news = get_news()
        decision_message = make_decision(news)
        last_context = decision_message
        send_message_to_telegram(decision_message)
        time.sleep(180)  # 30 minutes

# 💬 User message handler
@bot.message_handler()
def handle_user_message(message):
    query = message.text
    global last_context
    response = gemini_query(query, last_context)
    bot.send_message(message.chat.id, response)

if __name__ == "__main__":
    # Send the first news summary immediately
    initial_news = get_news()
    decision_message = make_decision(initial_news)
    last_context = decision_message
    send_message_to_telegram(decision_message)

    # Start scheduled news sending in a background thread
    thread = threading.Thread(target=start_sending_news)
    thread.start()

    # Start polling to listen for user messages
    print("Bot is polling...")
    bot.polling()
