import pandas as pd
import telebot
import os
from datetime import datetime
from telebot.types import InputMediaPhoto

# משיכת סודות
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def send_product():
    try:
        df = pd.read_excel('products.xlsx')
        
        # חישוב שורה (מחזורי לפי שעות)
        epoch = datetime(2024, 1, 1)
        now = datetime.now()
        hours_since_epoch = int((now - epoch).total_seconds() // 3600)
        index = hours_since_epoch % len(df)
        row = df.iloc[index]

        # הכנת הטקסט
        message_text = (
            f"🔥*{row['Name']}*\n\n"
            f"📦Description: {row['Description']}\n\n"
            f"Check it out👉: {row['Affiliate link']}"
        )

        # טיפול בתמונות - פירוק לפי הסימן |
        photo_links = str(row['Photos']).split('|')
        
        if len(photo_links) > 1:
            # אם יש כמה תמונות - יוצרים קבוצת מדיה
            media = []
            for i, link in enumerate(photo_links):
                # רק התמונה הראשונה מקבלת את הטקסט (ככה זה בטלגרם)
                caption = message_text if i == 0 else ""
                media.append(InputMediaPhoto(link.strip(), caption=caption, parse_mode='Markdown'))
            
            bot.send_media_group(CHAT_ID, media)
        else:
            # אם יש רק תמונה אחת
            bot.send_photo(CHAT_ID, photo_links[0].strip(), caption=message_text, parse_mode='Markdown')

        print(f"Sent product: {row['Name']} with {len(photo_links)} photos.")

    except Exception as e:
        print(f"!!! ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    send_product()
