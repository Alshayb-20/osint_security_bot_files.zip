
from flask import Flask, request
import requests
import re

app = Flask(__name__)

BOT_TOKEN = "7971093988:AAHkRgrinfOmv7lvom8mm_Dn6XaAL8BEEcU"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# دالة بسيطة لفحص البريد الإلكتروني
def is_email(text):
    return re.match(r"[^@]+@[^@]+\.[^@]+", text)

# دالة بسيطة لفحص رقم الهاتف (بداية + ورقم)
def is_phone(text):
    return re.match(r"^\+?\d{10,15}$", text)

# دالة البحث عن البيانات (مثال توعوي فقط)
def search_info(query):
    # هنا يمكن توصيل API حقيقية أو قواعد بيانات
    # مثال بيانات وهمية للشرح فقط:
    if is_email(query):
        return f"📧 البريد الإلكتروني: {query}\n🛡️ تم التحقق من صحة البريد."
    elif is_phone(query):
        return f"📱 رقم الهاتف: {query}\n🛡️ تم التحقق من صحة الرقم."
    else:
        return f"🔍 تم البحث عن: {query}\n⚠️ لا توجد بيانات دقيقة متاحة حالياً."

# إعداد أزرار الكيبورد
def main_keyboard():
    return {
        "keyboard": [
            ["بحث بواسطة رقم هاتف"],
            ["بحث بواسطة بريد إلكتروني"],
            ["بحث بواسطة اسم"],
            ["مساعدة"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "مرحباً! أرسل لي رقم هاتف أو بريد إلكتروني أو اسم للبحث.", reply_markup=main_keyboard())
        elif text in ["بحث بواسطة رقم هاتف", "بحث بواسطة بريد إلكتروني", "بحث بواسطة اسم"]:
            send_message(chat_id, f"يرجى إرسال {text} للبحث.")
        elif text == "مساعدة":
            send_message(chat_id, "يمكنك البحث عن بيانات باستخدام رقم الهاتف أو البريد الإلكتروني أو الاسم.")
        else:
            result = search_info(text)
            send_message(chat_id, result)

    return {"ok": True}

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=payload)

if __name__ == "__main__":
    app.run(port=5000)

