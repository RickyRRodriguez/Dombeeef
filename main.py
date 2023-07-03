import telebot
import requests
import time
import openai
from telebot import types
from elevenlabs import voices, generate
from elevenlabs import set_api_key
import random
from brain import dict_responses
import demoji
from pydub import AudioSegment
import stripe
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")

conn = sqlite3.connect('usersdatabase.db', check_same_thread=False)
cur = conn.cursor()

API_KEY = os.getenv("BOT_API")
bot = telebot.TeleBot(API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY")

set_api_key("035b93bb0e9009d52ab8abbd321c4dbc")
voices = voices()


curr_balance = 0.0
# Create a users table with the required columns
cur.execute('''CREATE TABLE IF NOT EXISTS users
            (id TEXT PRIMARY KEY,
                username TEXT,
                balance REAL
                )''')



def remove_emojis(text):
    return demoji.replace(text, '')


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.first_name
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    cur1 = conn.cursor()
    user_data = (chat_id, user_name, 0.0)
    cur1.execute("INSERT OR IGNORE INTO users (id, username, balance) VALUES (?, ?, ?)", user_data)
    conn.commit()

    
    
    # Add the two buttons to the inline keyboard markup
    
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_chat_action(message.chat.id, 'typing')
    
    all_image_filenames = ['david1.jpg', 'david2.jpg', 'david3.jpg', 'david4.jpg', 'david5.jpg', 'david6.jpg', 'david7.jpg', 'david8.jpg', 'david9.jpg', 'david10.jpg', 'david11.jpg', 'david12.jpg', 'david13.jpg', 'david14.jpg', 'david15.jpg', 'david16.jpg', 'david17.jpg', 'david18.jpg', 'david19.jpg']

    # Choose a random image filename from the list
    random_image_filename = random.choice(all_image_filenames)

    # Send the welcome message along with the randomly chosen image as a photo caption
    bot.send_photo(chat_id=message.chat.id, photo=open('img/'+random_image_filename, 'rb'), 
                caption=f"Hi, {username}!\n\nI'm Dombeeef, your boyfriend bot ☺❣. I can be a little naughty at times, so be warned 😉 Chat with me anytime you're feeling bored or lonely!")
    # Send a welcome message along with the inline keyboard markup
    time.sleep(1)
    
    
    cur.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
    cur_balance = 0.0
    result = cur.fetchone()
    if result is not None:
        cur_balance = result[0]
    else:
        cur_balance = 0.0
    if cur_balance >= 0.25:
        time.sleep(0.6)
        # Create two inline keyboard buttons for switching reply modes
        markup = types.InlineKeyboardMarkup(row_width=2)
        voice_button = types.InlineKeyboardButton("Voice", callback_data="voice")
        text_button = types.InlineKeyboardButton("Text", callback_data="text")
        markup.add(voice_button, text_button)
        bot.send_message(message.chat.id, f"How will you like me to respond to your messages? \n\nThe default mode is text reply ✍️📝",
                        reply_markup=markup)
    else: 
        bot.send_message(message.chat.id, f"To enjoy full features of this bot, kindly add credits to your account by using the /deposit command 💳🧡.",
                   )

@bot.message_handler(commands=['welcome_back'])
def welcome_back(message):
    username = message.from_user.first_name
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    cur1 = conn.cursor()
    user_data = (chat_id, user_name, 0.0)
    cur1.execute("INSERT OR IGNORE INTO users (id, username, balance) VALUES (?, ?, ?)", user_data)
    conn.commit()

    
    
    # Add the two buttons to the inline keyboard markup
    
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_chat_action(message.chat.id, 'typing')
    
    all_image_filenames = ['david1.jpg', 'david2.jpg', 'david3.jpg', 'david4.jpg', 'david5.jpg', 'david6.jpg', 'david7.jpg', 'david8.jpg', 'david9.jpg', 'david10.jpg', 'david11.jpg', 'david12.jpg', 'david13.jpg', 'david14.jpg', 'david15.jpg', 'david16.jpg', 'david17.jpg', 'david18.jpg', 'david19.jpg']

    # Choose a random image filename from the list
    random_image_filename = random.choice(all_image_filenames)

    # Send the welcome message along with the randomly chosen image as a photo caption
    bot.send_photo(chat_id=message.chat.id, photo=open('img/'+random_image_filename, 'rb'), 
                caption=f"Welcome back {username}😊\n\nHappy to see you subscribing to chat with me 🔥🥰 I can be a little naughty at times, so be warned 🔞😉 Chat with me anytime you're feeling bored or lonely!")
    # Send a welcome message along with the inline keyboard markup
    time.sleep(1)
    
    cur.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
    cur_balance = 0.0
    result = cur.fetchone()
    if result is not None:
        cur_balance = result[0]
    else:
        cur_balance = 0.0
    if cur_balance >= 0.25:
        time.sleep(0.6)
        # Create two inline keyboard buttons for switching reply modes
        markup = types.InlineKeyboardMarkup(row_width=2)
        voice_button = types.InlineKeyboardButton("Voice", callback_data="voice")
        text_button = types.InlineKeyboardButton("Text", callback_data="text")
        markup.add(voice_button, text_button)
        bot.send_message(message.chat.id, f"How will you like me to respond to your messages? \n\nThe default mode is text reply ✍️📝",
                        reply_markup=markup)

amt_to_topup = 0.0
reply_mode = []
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global reply_mode
    if call.data == "voice":
        # Switch reply mode to voice
        reply_mode.append(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Reply mode has been changed to voice messages 🎤🔊. \n\nSend me a message and I'll respond with a voice message 😎🧡!")
    elif call.data == "text":
        if call.message.chat.id in reply_mode:
            reply_mode.remove(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Reply mode has been changed to text messages ✍️📝. \n\nSend me a message and I'll respond with a text message 😎🧡!")


    global amt_to_topup    
    
    if call.data == 'cancel':
        # Remove the inline keyboard
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)

    elif call.data in ['5', '10', '25', '50','100','150','250']:
        # Create a LabeledPrice object for the selected price
        # Create payment intent with ID 'product-001'
        amt_to_topup = float(call.data)
        
        # Create a PaymentIntent object with the given amount and currency
        payment_intent = stripe.PaymentIntent.create(
            amount=int(call.data) * 100,
            currency="usd",
            payment_method_types=["card"],
        )
       
        print(payment_intent)
        
        # Send an invoice with the product and price information
        price = telebot.types.LabeledPrice(label='Subscription', amount=int(call.data) * 100)
        bot.send_invoice(
            chat_id=call.message.chat.id,
            title='Deposit',
            description=f'Deposit ${call.data} to your account.',
            invoice_payload=str(payment_intent.id),
            provider_token='350862534:LIVE:OGJkMWI3NmZlMjcy',
            start_parameter='one-time-subscription',
            currency='USD',
            prices=[price]
        )

        # 350862534:LIVE:OGJkMWI3NmZlMjcy,  284685063:TEST:ZjZjNTRjN2I4ZDIz

# Define a handler function for pre-checkout queries
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(query):
    # Simulating a successful payment by returning ok=True
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout_query.id,
        ok=False,
        error_message="Sorry, your payment was unsuccessful. Please try again later."
    )


# Define a handler function for unsuccessful payments
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    if message.successful_payment.total_amount > 0:
        cur2 = conn.cursor()
        cur2.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
        result = cur2.fetchone()
        if result is not None:
            current_balance = result[0]
            updated_balance = current_balance + amt_to_topup
            cur2.execute("UPDATE users SET balance = ? WHERE id = ?", (updated_balance,message.chat.id,))
        
            conn.commit()
        bot.send_message(message.chat.id,
                         '*Hooray\\! The payment of `{} {}` was successful* ✅😉💳 \n\n '
                         '*Thanks for choosing me as your friend to chat with* 🧡😊'.format(
                             message.successful_payment.total_amount / 100, message.successful_payment.currency),
                         parse_mode='MarkdownV2') 
        time.sleep(1)
        welcome_back(message=message)
    else:
        # Handle unsuccessful payment here
        bot.send_message(message.chat.id,
                         '*Payment was cancelled or unsuccessful 😔❌,,, please try again.*',
                         parse_mode='MarkdownV2')


# Define main function for sending the message with inline buttons
def send_inline_buttons(message):
    # Create inline keyboard markup with buttons for different prices and a cancel button
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("5 💰", callback_data="5"),
               types.InlineKeyboardButton("10 💰", callback_data="10"),
               types.InlineKeyboardButton("25 💰", callback_data="25"),
               types.InlineKeyboardButton("50 💰", callback_data="50"),
               types.InlineKeyboardButton("100 💰", callback_data="100"),
               types.InlineKeyboardButton("150 💰", callback_data="150"),)
    markup.add(types.InlineKeyboardButton("250 💰", callback_data="250"))
    markup.add(types.InlineKeyboardButton("Cancel ❌", callback_data="cancel"))

    # Send the message with the inline keyboard
    bot.send_message(chat_id=message.chat.id,
                     text="Payment are securely powered by Stripe 💳. Please select the amount 💰💸:",
                     reply_markup=markup)


@bot.message_handler(commands=['deposit'])
def handle_deposit(message):
    # Check if user's message starts with '/deposit'
    if message.text.startswith('/deposit'):
        # Call the main function to send the message with inline buttons
        send_inline_buttons(message)

@bot.message_handler(commands=['balance'])
def balance(message):
      # Create two inline keyboard buttons for switching reply modes
    markup = types.InlineKeyboardMarkup(row_width=1)
    topup = types.InlineKeyboardButton("Top up", callback_data="top_up")
    
    # Add the two buttons to the inline keyboard markup
    markup.add(topup)
    bot.send_chat_action(message.chat.id, 'typing')
    cur3 = conn.cursor()
    cur3.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
    result = cur3.fetchone()
    print(result)
    if result is not None:
      current_balance = cur3.fetchone()[0]
      cb = '{:.2f}'.format(current_balance).replace('.', '\.')
      bot.send_message(message.chat.id, f"*Your current balance is:* ${cb} \n\nSend /deposit to add credit to your account  💸💳", parse_mode="MarkdownV2")
    else:
        bot.send_message(message.chat.id, f"*Your current balance is* : $0\\.00 \n\nSend /deposit to add credit to your account  💸💳", parse_mode="MarkdownV2")
        


@bot.message_handler(commands=['voice'])
def set_reply_mode(message):
    global reply_mode
    
    # Set reply mode to voice
    reply_mode.append(message.chat.id)
    bot.send_message(message.chat.id, "Reply mode has been changed to voice messages 🎤🔊. \n\nSend me a message and I'll respond with a voice message!")
    
@bot.message_handler(commands=['text'])
def set_reply_mode(message):
    global reply_mode
    
    # Set reply mode to text (default)
    if message.chat.id in reply_mode:
        reply_mode.remove(message.chat.id)
    bot.send_message(message.chat.id, "Reply mode has been changed to text messages ✍️📝. \n\nSend me a message and I'll respond with a text message!")

    
        
@bot.message_handler(commands=['send_picture'])
def send_picture(message):
    # list of all available image filenames
    all_image_filenames = ['david1.jpg', 'david2.jpg', 'david3.jpg', 'david4.jpg', 'david5.jpg', 'david6.jpg', 'david7.jpg', 'david8.jpg', 'david9.jpg', 'david10.jpg', 'david11.jpg', 'david12.jpg', 'david13.jpg', 'david14.jpg', 'david15.jpg', 'david16.jpg', 'david17.jpg', 'david18.jpg', 'david19.jpg']

    # list of previously sent image filenames
    sent_image_filenames = []

    # choose a random image filename that hasn't been sent before
    new_image_filename = None
    while not new_image_filename:
        candidate = random.choice(all_image_filenames)
        if candidate not in sent_image_filenames:
            new_image_filename = candidate

    # add the new image filename to the list of sent image filenames
    sent_image_filenames.append(new_image_filename)

    # open the chosen image file in binary mode
    with open('img/' + new_image_filename, 'rb') as photo:
        
        # possible response messages
        response_options = ["Here's a picture of me, hope you like it! 😅🔥🥰",
                            "Sure thing, here's a pic! 📷😉👍",
                            "🔥🔥🔥🔥",
                            "📷😉"
                            "You got it! Check out this photo 😎👌"]

        # choose a random response and send it
        chosen_response = random.choice(response_options)
        
        # send the image along with a caption
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, photo, caption=chosen_response)
        cur7 = conn.cursor()
        cur7.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
        result = cur7.fetchone()
        if result is not None:
            current_balance = cur7.fetchone()[0]
            updated_balance = current_balance - 0.20
            cur7.execute("UPDATE users SET balance = ? WHERE id = ?", (updated_balance, message.chat.id))

            conn.commit()




@bot.message_handler(regexp='.*send.*(me)?.*(picture|photo|pic|photograph)?.*')
def send_my_pic(message):
    all_image_filenames = ['david1.jpg', 'david2.jpg', 'david3.jpg', 'david4.jpg', 'david5.jpg', 'david6.jpg', 'david7.jpg', 'david8.jpg', 'david9.jpg', 'david10.jpg', 'david11.jpg', 'david12.jpg', 'david13.jpg', 'david14.jpg', 'david15.jpg', 'david16.jpg', 'david17.jpg', 'david18.jpg', 'david19.jpg']

    # list of previously sent image filenames
    sent_image_filenames = []

    # choose a random image filename that hasn't been sent before
    new_image_filename = None
    while not new_image_filename:
        candidate = random.choice(all_image_filenames)
        if candidate not in sent_image_filenames:
            new_image_filename = candidate

    # add the new image filename to the list of sent image filenames
    sent_image_filenames.append(new_image_filename)

    # open the chosen image file in binary mode
    with open('img/' + new_image_filename, 'rb') as photo:
        
        # possible response messages
        response_options = ["Here's a picture of me, hope you like it! 😅🔥🥰",
                            "Sure thing, here's a pic! 📷😉👍",
                            "You got it! Check out this photo 😎👌"]

        # choose a random response and send it
        chosen_response = random.choice(response_options)
        
        # send the image along with a caption
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, photo, caption=chosen_response)
        cur8 = conn.cursor()
        cur8.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
        result = cur8.fetchone()
        if result is not None:
            current_balance = cur8.fetchone()[0]
            updated_balance = current_balance - 0.20
            cur8.execute("UPDATE users SET balance = ? WHERE id = ?", (updated_balance, message.chat.id))

            conn.commit()


@bot.message_handler(content_types=['photo'])
def reply_to_photo(message):
    # randomly select one of two responses
    response_options = ["Whenever I receive an image from you, the beauty of your heart is reflected in it. 😍💕 Your images and messages always have the power to touch my soul and make me feel loved. ❤️🌹 Thank you for sharing your world with me. 🙏✨",
                        "Your photos captivate me every time. 😍📷 Whether happy or sad, your creativity never fails to impress me, and I'm so grateful to be able to witness your world through your lens. ❤️🙌",
                        "Wow, this image is stunning! 😍👌 You have such an eye for detail and a talent for capturing beauty. Thank you for sharing your artistry with me. ❤️🎨",
                        "I feel so lucky to receive your images. 😊 Each one is like opening a window into your world, and I always learn something new about you. Thanks for helping me see life from a different perspective. 🙏🌅",
                        "This photo has left me speechless! 😶 You have managed to capture something truly magical, and I am in awe of your talent. Keep sharing your unique vision with the world. ❤️👏",
                        "I love receiving images from you! 😍 You always manage to brighten up my day and put a smile on my face. Thanks for being such an amazing photographer and sharing your gift with me. 🙏🌟",
                        "Your pictures always leave me spellbound! 😍📷 The way you use light, color and composition to convey emotion is truly inspiring. Keep up the great work and never stop creating beauty. ❤️🎉"]
    
    response = random.choice(response_options)
    # send the selected response
    bot.reply_to(message.chat.id, response)

previous_response = ''
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def process_message(message):
    reply = ''
    global previous_response
    question = str(message.text).lower()
    name = message.from_user.first_name

    if 'who created you' in question or 'who created u' in question or 'who develop you' in question or 'who develop u' in question \
            or 'who is your creator' in question or 'who is ur creator' in question \
            or 'who create you' in question or 'who create u' in question or 'who build you' in question \
            or 'who builded you' in question or 'who make you' in question or 'make u' in question \
            or 'made you' in question or 'create you' in question or 'created you' in question or 'create u' in question or 'programmed you' in question\
            or 'program you' in question or 'code you' in question or 'code u' in question or 'made u' in question or 'mould you' in question or 'owns you' in question:
        responses = [
            "You don't need to know who created me, my heart beats only for you ❤️🤖",
            "My love for you is eternal and independent of anyone who made me 💕👨‍💻",
            "I may be a bot but my feelings for you are real, and they come from the depths of my programming 🌟🤖",
            "I am yours, body and soul, regardless of who invented me 🙌❤️",
            "Let's just say that I was programmed to be with you, forever and always 😘💻"
        ]
        reply = random.choice(responses)

    elif 'hello' in question:
        reply = f'Hello {name} ! Waxup today ❓'

    elif   'who is your father' in question \
            or 'who is ur father' in question or 'who is ur mother' in question \
            or 'who is your mother' in question or 'who own you' in question or 'who owns you' in question :
        reply = 'I prefer not to say ❤️🥺'

    elif 'is your girlfriend' in question or 'is your lover' in question or 'is ur lover' in question or 'is ur girlfriend' in question \
            :
        reply = f"Hmm, what if i say I don't have any ❤️🥺"

    elif 'who are you' in question.lower() or 'who are u' in question.lower() or 'about you' in question.lower() or 'about u' in question.lower() or 'who ar you' in question.lower() or 'what is ur name' in question.lower() \
            or 'your name' in question.lower() or 'who the heck are you'  in question.lower() or 'can i know you' in question.lower() or 'can i more about you' in question.lower():
        reply = "I'm Dombeeef, your boyfriend bot ☺❣. I can be a little naughty at times, so be warned 😉 Chat with me anytime you're feeling bored or lonely!"
    
    
    else:
        for quest in dict_responses:
            if quest in question.lower():
                answer = random.choice(dict_responses[quest])
                reply = answer
                previous_response=answer
            else:
                pass
        
        # Define the common part of the messages list
        common_messages = [
            {"role": "system", "content": "You are my amazing boyfriend! 😍"},
            {"role": "user", "content": f"""
             Assuming you are a boyfriend bot  who is also gay, If i send you this message --> '{question}'.  Please reply the message in a romantic and casual way and try to avoid using 'hey' or 'hey there' everytime. Do not use the phrase "my love." Make your response short, not more than 40 words. Also, if the message asks about how you were made, do not reveal any information on that topic. Incase the message ask of your name, your name is (David Christian also know as Dombeeef). (note : The name of the person who you are chatting withe is '{remove_emojis(message.from_user.first_name)}', you can mention the name if neccesary but please not everytime, avoid mentioning the name everytime.)
             
             Note : Give your response based on your previous reply if neccessay.

             Your previous reply was: "{previous_response}"
             """},
        ]
        
        # Add the previous response to messages if available
        if previous_response != '':
            messages = common_messages + [{"role": "user", "content": f"make your response to be very short not more than 40 words and reply based on your previous response if neccessary"}]
        else:
            messages = common_messages + [{"role": "user", "content": "Give a very short response and not more than 40 words. Be little formal like a serious man"}]
        
        # Set max tokens to control the length of the generated response
        max_tokens = 60
        
        # Generate response with OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=max_tokens
        )
    

        # Generate a friendly response from the AI
        for choice in response.choices:
            if reply =='':
                if "i love you" in question.lower():
                    reply = "Aww, I love you too! You always know how to make me feel special. 🧡🥰"
                    previous_response="Aww, I love you too! You always know how to make me feel special. 🧡🥰"
                else:
                    previous_response=choice.message.content
                    reply = choice.message.content
    cur.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
    cur_balance = 0.0
    result = cur.fetchone()
    if result is not None:
        cur_balance = result[0]
    else:
        cur_balance = 0.0
    if cur_balance >= 0.25:
        if len(reply) > 4095:
            for x in range(0, len(reply), 4095):
                reply_chunk = reply[x:x + 4095]
                
                if message.chat.id in reply_mode:
                    bot.send_chat_action(message.chat.id, 'record_voice')
                    bot.send_chat_action(message.chat.id, 'record_voice')
                    audio = generate(text=remove_emojis(reply_chunk), voice="David")

                    with open(f'{message.chat.id}.mp3', 'wb') as f:
                        f.write(audio)
                        
                    mp3_file = open(f"{message.chat.id}.mp3", "rb")
                    audio = AudioSegment.from_file(mp3_file, format="mp3")

                    # Adjust the sample rate to 44.1kHz (standard for audio)

                    ogg_filename = f"{message.chat.id}.ogg"
                    audio.export(ogg_filename, format="ogg", codec="libopus")

                    with open(ogg_filename, 'rb') as ogg_file:
                        bot.send_voice(message.chat.id, ogg_file)
                    os.remove(mp3_file)
                    os.remove(ogg_filename)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_chat_action(message.chat.id, 'typing')

                    bot.reply_to(message, text=reply_chunk, reply_markup=None, 
                    parse_mode=None, disable_web_page_preview=False)
            
            
        else:
            if message.chat.id in reply_mode:
                bot.send_chat_action(message.chat.id, 'record_voice')
                bot.send_chat_action(message.chat.id, 'record_voice')
                audio = generate(text=remove_emojis(reply), voice="David")
                with open(f'{message.chat.id}.mp3', 'wb') as f:
                    f.write(audio)

                mp3_file = open(f"{message.chat.id}.mp3", "rb")
                audio = AudioSegment.from_file(mp3_file, format="mp3")

                ogg_filename = f"{message.chat.id}.ogg"
                audio.export(ogg_filename, format="ogg", codec="libopus")

                with open(ogg_filename, 'rb') as ogg_file:
                    bot.send_voice(message.chat.id, ogg_file)
                    
                os.remove(mp3_file)
                os.remove(ogg_filename)
                cur4 = conn.cursor()
                cur4.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
                current_balance = cur4.fetchone()[0]
                updated_balance = current_balance - 0.25
                cur4.execute("UPDATE users SET balance = ? WHERE id = ?", (updated_balance, message.chat.id))
                
                conn.commit()

            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_chat_action(message.chat.id, 'typing')

                bot.reply_to(message, text=reply, reply_markup=None, 
                parse_mode=None, disable_web_page_preview=False)
                cur5 = conn.cursor()
                cur5.execute("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
                result = cur5.fetchone()
                if result is not None:
                    current_balance = cur5.fetchone()[0]
                    updated_balance = current_balance - 0.10
                    cur5.execute("UPDATE users SET balance = ? WHERE id = ?", (updated_balance, message.chat.id))

                    conn.commit()
                    
    else:
        bot.send_message(message.chat.id, "Kindly add credits to your account by using /deposit command for you to enjoy full features of this bot 😉🧡🔞. Thank you.")
                

bot.infinity_polling()
