from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Token from env variable
URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
AUTHORIZED_USERS = [6356015122]

def send_message(chat_id, text, reply_to=None, buttons=None):
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    if reply_to:
        data['reply_to_message_id'] = reply_to
    if buttons:
        data['reply_markup'] = buttons
    requests.post(URL + 'sendMessage', json=data)

def get_buttons():
    return {
        "inline_keyboard": [[
            {"text": "🔓 Appeal", "url": "https://t.me/TeamTelegram"},
            {"text": "ℹ️ Learn More", "url": "https://telegram.org/faq"},
            {"text": "💬 Support", "url": "https://t.me/spambot"}
        ]]
    }

@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update:
        msg = update['message']
        text = msg.get('text', '')
        chat_id = msg['chat']['id']
        user = msg['from']
        user_id = user['id']
        first_name = user['first_name']
        msg_id = msg['message_id']

        # /auth command
        if text.startswith('/auth'):
            if user_id in AUTHORIZED_USERS:
                send_message(chat_id, f"✅ You are an authorized developer, *{first_name}*!", msg_id)
            else:
                send_message(chat_id, "❌ You are *not authorized* to use this bot.", msg_id)
            return 'ok'

        # Check if user is authorized for dangerous commands
        if text.startswith(('/',)):
            if user_id not in AUTHORIZED_USERS:
                send_message(chat_id, "❌ *Access Denied!*\nYou are not authorized to use this command.", msg_id)
                return 'ok'

        # Dangerous prank commands
        if text.startswith('/bn'):
            send_message(chat_id,
                f"⚠️ *[System Alert]* ⚠️\n\nUser `{first_name}` has been *banned* from all Telegram **Groups** and **Channels**.\n\n*Reason:* 🚫 Suspicious Activity Detected\n\n⛔ Access Revoked\n🧨 Appeals Blocked\n\n🔒 *Effective Immediately!*",
                msg_id, buttons=get_buttons())

        elif text.startswith('/rs'):
            send_message(chat_id,
                f"🚫 *[Telegram Security Notice]* 🚫\n\nYour account has been *temporarily restricted*.\n\n📅 Date: *Today*\n🔍 Reason: _Unusual behavior patterns detected_\n\n⏳ *Messaging, Joining & Forwarding limited until further notice*",
                msg_id, buttons=get_buttons())

        elif text.startswith('/warn'):
            send_message(chat_id,
                f"⚠️ *Final Warning Issued* ⚠️\n\nUser `{first_name}` has received their *last warning* for violating Telegram's policies.\n\n📢 Next offense will result in *account deletion.*",
                msg_id, buttons=get_buttons())

        elif text.startswith('/privacy_check'):
            send_message(chat_id,
                f"🔍 *Privacy Review In Progress*\n\nTelegram is currently reviewing your recent activity.\n\n⏱️ Please wait while your account status is being verified.\n\n🔐 Any unusual behavior may lead to *temporary lockout*.",
                msg_id, buttons=get_buttons())

        elif text.startswith('/limit'):
            send_message(chat_id,
                f"⛔ *Account Limitation Notice* ⛔\n\nDear `{first_name}`, your Telegram account has been *limited* for the next *7 days* due to violation of community terms.\n\n⚠️ Limited access includes:\n- Messaging\n- Group joining\n- Bot usage\n\n📅 Limitation will auto-expire after *7 days* unless re-evaluated.",
                msg_id, buttons=get_buttons())

        elif text.startswith('/block'):
            send_message(chat_id,
                f"❌ *Account Blocked Permanently* ❌\n\nDear `{first_name}`, your Telegram account has been *permanently blocked*.\n\n🛑 Reason: Multiple severe violations\n🕵️‍♂️ Account under review\n\n📵 You can no longer use Telegram services.",
                msg_id, buttons=get_buttons())

    return 'ok'
