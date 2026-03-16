import pandas as pd
import telebot
import os
from datetime import datetime

# הגדרות - את ה-Token וה-Chat ID נשמור ב-Secrets של GitHub
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def send_product():
    # קריאת קובץ האקסל (נניח ששמו products.xlsx)
    df = pd.read_excel('products.xlsx')
    
    # חישוב איזה מוצר לשלוח על בסיס הזמן (כדי שזה יהיה מחזורי)
    # נשתמש במספר השעות שעברו מאז תאריך מסוים כדי שזה תמיד יתקדם
    epoch = datetime(2024, 1, 1) # תאריך שרירותי בעבר
    now = datetime.now()
    hours_since_epoch = int((now - epoch).total_seconds() // 3600)
    
    # בחירת השורה (מודולו אורך הטבלה כדי לחזור להתחלה)
    index = hours_since_epoch % len(df)
    row = df.iloc[index]

    # הכנת ההודעה (באנגלית כפי שביקשת)
    message_text = (
        f"*{row['Name']}*\n\n"
        f"Description: {row['Description']}\n\n"
        f"Check it out: {row['Affilate link']}"
    )

    # שליחת התמונה (מלינק) עם הטקסט מתחתיה
    try:
        bot.send_photo(CHAT_ID, row['Photos'], caption=message_text, parse_mode='Markdown')
        print(f"Sent product: {row['Name']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_product()
