import os
import subprocess
import logging
import http.server
import threading
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8255416395:AAE_xskTzY32rhq6hwNWw5qWPD3OC1xqg4o"

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ /generate ကိုနှိပ်ပြီး အလုပ်လုပ်မယ့် Config ထုတ်နိုင်ပါတယ်။")

async def generate_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("Config အသစ် ထုတ်ပေးနေပါတယ်။ ခဏစောင့်ပါ...")

    os.chdir("/tmp")

    try:
        # Register and Generate
        subprocess.run(["/usr/local/bin/wgcf", "register", "--accept-tos"], check=True)
        subprocess.run(["/usr/local/bin/wgcf", "generate"], check=True)
        
        file_path = "/tmp/wgcf-profile.conf"
        
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()

            # --- အရေးကြီးတဲ့ ပြင်ဆင်မှုများ ---
            # ၁။ MTU ကို 1280 ပြောင်းမယ် (Connection ပိုမြဲဖို့)
            content = re.sub(r'MTU = .+', 'MTU = 1280', content)
            
            # ၂။ Endpoint ကို မြန်မာပြည်မှာ အလုပ်လုပ်တဲ့ IP တစ်ခုနဲ့ အစားထိုးကြည့်မယ်
            # engage.cloudflareclient.com အစား IP တိုက်ရိုက် သုံးကြည့်ခြင်း
            content = content.replace('engage.cloudflareclient.com:2408', '162.159.193.5:2408')

            new_file_path = f"/tmp/WARP_{user_id}.conf"
            with open(new_file_path, "w") as f:
                f.write(content)

            # Send the updated file
            with open(new_file_path, "rb") as file:
                await context.bot.send_document(chat_id=user_id, document=file, filename=f"WARP_{user_id}.conf")
            
            # Clean up
            os.remove("/tmp/wgcf-account.json")
            os.remove("/tmp/wgcf-profile.conf")
            os.remove(new_file_path)
        else:
            await update.message.reply_text("Error: Config ဖိုင် မထုတ်ပေးနိုင်ပါ။")
        
    except Exception as e:
        await update.message.reply_text(f"Error တက်သွားပါတယ်: {str(e)}")

def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_config))
    app.run_polling()

if __name__ == "__main__":
    main()
