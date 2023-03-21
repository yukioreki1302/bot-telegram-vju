#Code Chính Thức Chạy Bot Telegram
#Dev By H.K

import telebot
import signal
import sys
from telebot import types
import random

# Enable Bot = TOKEN. Multiple BOTs can be activated by spamming multiple bot commands = telebot.TeleBot("BOT ID")
bot = telebot.TeleBot("5997677492:AAHLrqLXH6Oyu1_QIf98W3eQFYCZLkbZ0jI")

# Initialize a global variable to store the account's balance
account_balance = 0

# Save the OTP in the global variable
global confirmation_code
confirmation_code = None

# Check VS CODE -> telegram connection by sending Bot notification message to user ID
user_ids = ["6233623714"]
user_ids = ["6042907090"]
user_ids = ["5078672068"]
user_ids = ["5601284498"]
# user_ids = ["-1001616591003"]

message = "Xin chào, tôi là Chatbot của Team DV HKT! Hãy chat lệnh: /start để bắt đầu"
for user_id in user_ids:
    bot.send_message(user_id, message)
print("Đã gửi tin nhắn thành công!")

# Create Inline Keyboard command buttons for help, account_info and topup commands
def create_inline_keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    row1 = [types.InlineKeyboardButton(text='Thông tin tài khoản', callback_data='account_info'),
            types.InlineKeyboardButton(text='Nạp tiền', callback_data='topup')]
    row2 = [types.InlineKeyboardButton(text='Chuyển Tiền', callback_data='transfer'),
            types.InlineKeyboardButton(text='Lịch Sử Giao dịch', callback_data='transaction_history')]
    row3 = [types.InlineKeyboardButton(text='Trợ giúp', callback_data='help')]
    inline_keyboard.row(*row1)
    inline_keyboard.row(*row2)
    inline_keyboard.row(*row3)
    return inline_keyboard

# Handle callback from Inline Keyboard button
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'account_info':
        send_account_info(call.message)
    elif call.data == 'topup':
        handle_topup(call.message)
    elif call.data == 'transfer':
       handle_transfer_money(call.message)
    elif call.data == 'transaction_history':
       handle_transaction_history(call.message)
    elif call.data == 'help':
        send_help(call.message)    
    bot.answer_callback_query(callback_query_id=call.id)
    #bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)


# Command /start 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Xin chào, đây là B.O.T của Team DV HKT!"
                          "Vui lòng chọn các lệnh bên dưới mà Bot có thể thực hiện:", reply_markup=create_inline_keyboard()) 

# Command /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Hiện tại chưa cập nhận được trợ giúp mong bạn thông cảm!")

# Command /account_info   
@bot.message_handler(commands=['account_info'])
def send_account_info(message):
    chat_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    formatted_balance = "{:,.0f}".format(account_balance).replace(",", " ")
    bot.send_message(chat_id, f"Username: {username}\nFirst name: {first_name}\nLast name: {last_name}\nSố dư tài khoản: {formatted_balance} VNĐ")

# Command /topup
@bot.message_handler(commands=['topup'])
def handle_topup(message):
    chat_id = message.chat.id
    # Generate random confirmation OTP code
    global confirmation_code
    confirmation_code = random.randint(1000, 9999)
    # Require the user to enter a confirmation code
    bot.send_message(chat_id, f"Không chia sẻ OTP này với bất kỳ ai. Mã OTP của bạn là {confirmation_code}. \nVui lòng nhập mã OTP để xác nhận giao dịch nạp tiền")
    # Switch to waiting state to enter confirmation code
    bot.register_next_step_handler(message, process_confirm_topup)

def process_confirm_topup(message):
    chat_id = message.chat.id
    try:
        # Get the user-entered confirmation code and check
        confirm_code = int(message.text)
        global confirmation_code
        if confirm_code == confirmation_code:
            # If the verification code is correct, continue with the deposit process
            bot.send_message(chat_id, "Mã xác nhận chính xác, vui lòng nhập số tiền nạp:")
            # Switch to waiting state to enter the deposit amount
            bot.register_next_step_handler(message, process_topup)
        else:
            # If the confirmation code is wrong, ask to re-enter it
            bot.send_message(chat_id, "Mã OTP không chính xác. Vui lòng thử lại.")
    except ValueError:
        bot.send_message(chat_id, "Mã OTP không hợp lệ. Vui lòng thử lại.")

def process_topup(message):
    chat_id = message.chat.id
    try:
        amount = float(message.text)
        if amount <= 0:  # Check if the amount entered is not greater than 0
            bot.send_message(chat_id, "Bạn đã nhập sai vui lòng nhập lại!")
        else:
            global account_balance
            account_balance += amount
            formatted_amount = "{:,.0f}".format(amount).replace(",", " ")
            formatted_balance = "{:,.0f}".format(account_balance).replace(",", " ")
            bot.send_message(chat_id, f"Bạn đã nạp thành công: {formatted_amount} VND. Số dư hiện tại của bạn là: {formatted_balance} VND.")
    except ValueError:
        bot.send_message(chat_id, "Số tiền không hợp lệ. Vui lòng nhập lại.")

# 
# Command / transfer money
@bot.message_handler(commands=['transfer'])
def handle_transfer_money(message):
    chat_id = message.chat.id
    # Generate random confirmation OTP code
    global confirmation_code
    confirmation_code = random.randint(1000, 9999)
    # Require the user to enter a confirmation code
    bot.send_message(chat_id, f"Không chia sẻ OTP này với bất kỳ ai. Mã OTP của bạn là {confirmation_code}. \nVui lòng nhập mã OTP để xác nhận giao dịch chuyển tiền")
    # Switch to waiting state to enter confirmation code
    bot.register_next_step_handler(message, process_confirm_transfer)

def process_confirm_transfer(message):
    chat_id = message.chat.id
    try:
        # Get the user-entered confirmation code and check
        confirm_code = int(message.text)
        global confirmation_code
        if confirm_code == confirmation_code:
            # If the verification code is correct, continue with the deposit process
            bot.send_message(chat_id, "Mã xác nhận chính xác, vui lòng nhập số tiền chuyển:")
            # Switch to waiting state to enter the deposit amount
            bot.register_next_step_handler(message, process_transfer)
        else:
            # If the confirmation code is wrong, ask to re-enter it
            bot.send_message(chat_id, "Mã xác nhận không chính xác. Vui lòng thử lại.")
    except ValueError:
        bot.send_message(chat_id, "Mã xác nhận không hợp lệ. Vui lòng thử lại.")

def process_transfer(message):
    chat_id = message.chat.id
    try:
        amount = float(message.text)
        global account_balance
        if amount <= 0:  # Check if the amount entered is not greater than 0
            bot.send_message(chat_id, "Bạn đã nhập sai vui lòng nhập lại!")
        elif amount > account_balance:  # check if the amount entered is not greater than the balance
            bot.send_message(chat_id, "Số dư của bạn không đủ, Vui lòng Nhập lại")
        else:
            account_balance -= amount
            formatted_amount = "{:,.0f}".format(amount).replace(",", " ")
            formatted_balance = "{:,.0f}".format(account_balance).replace(",", " ")
            bot.send_message(chat_id, f"Bạn đã chuyển thành công: {formatted_amount} VND. Số dư hiện tại của bạn là: {formatted_balance} VND.")
    except ValueError:
        bot.send_message(chat_id, "Số tiền không hợp lệ. Vui lòng nhập lại.")

# Command / Transaction history
@bot.message_handler(commands=['transaction_history'])
def handle_transaction_history(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Khi nào rảnh rồi làm lịch sử giao dịch sau")
#     Generate random confirmation OTP code
#     global confirmation_code
#     confirmation_code = random.randint(1000, 9999)
#     # Require the user to enter a confirmation code
#     bot.send_message(chat_id, f"Không chia sẻ OTP này với bất kỳ ai. Mã OTP của bạn là {confirmation_code}. \nVui lòng nhập mã OTP để xác nhận mở lịch sử giao dịch")
#     # Switch to waiting state to enter confirmation code
#     bot.register_next_step_handler(message, process_confirm_transaction_history)

# def process_confirm_transaction_history(message):
#     # Cần sử dụng Data base để chuyển từ ID này sang ID khác
#     chat_id = message.chat.id
#     try:
#         # Get the user-entered confirmation code and check
#         confirm_code = int(message.text)
#         global confirmation_code
#         if confirm_code == confirmation_code:
#             # If the verification code is correct, continue with the deposit process
#             bot.send_message(chat_id, "Mã xác nhận chính xác")
#             bot.send_message(chat_id, "Khi nào rảnh rồi làm lịch sử giao dịch sau")
#             # Switch to waiting state to enter the deposit amount
#             bot.register_next_step_handler(message, process_transaction_history)
#         else:
#             # If the confirmation code is wrong, ask to re-enter it
#             bot.send_message(chat_id, "Mã OTP không chính xác. Vui lòng thử lại.")
#     except ValueError:
#         bot.send_message(chat_id, "Mã OTP không hợp lệ. Vui lòng thử lại.")

# def process_transaction_history(message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, "Khi nào rảnh rồi làm lịch sử giao dịch sau")
#     #  Sử dụng My SQL
    
# Handle all other messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def stop_bot(signal, frame):
    print('Stopping bot')
    sys.exit(0)

# Handle keyboard signals to stop bots
signal.signal(signal.SIGINT, stop_bot)

# Run bot continuously
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        bot.stop_polling()
