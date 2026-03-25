import os
import subprocess
import http.server
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8255416395:AAE_xskTzY32rhq6hwNWw5qWPD3OC1xqg4o"

# Render မပိတ်သွားအောင် dummy port တစ်ခု ဖွင့်ထားပေးခြင်း
def run_dummy_server():
    server_address = ('', int(os.environ.get("PORT", 8080)))
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ /generate ကိုနှိပ်ပြီး Wireguard Config ထုတ်နိုင်ပါတယ်။")

async def generate_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("Config ထုတ်ပေးနေပါတယ်။ ခဏစောင့်ပါ...")

    # ဖိုင်တွေကို /tmp/ ထဲမှာပဲ လုပ်ပါ (Render မှာ ဒါမှ အဆင်ပြေမှာပါ)
    os.chdir("/tmp")

    try:
        # wgcf register and generate
        subprocess.run(["wgcf", "register", "--accept-tos"], check=True)
        subprocess.run(["wgcf", "generate"], check=True)
        
        file_path = "/tmp/wgcf-profile.conf"
        
        # Send the file
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                await context.bot.send_document(chat_id=user_id, document=file, filename=f"WARP_{user_id}.conf")
            
            # Clean up
            os.remove("/tmp/wgcf-account.json")
            os.remove(file_path)
        else:
            await update.message.reply_text("ဖိုင်ထုတ်ယူရာမှာ အမှားအယွင်းရှိနေပါတယ်။")
        
    except Exception as e:
        await update.message.reply_text(f"Error တက်သွားပါတယ်: {str(e)}")

def main():
    # Dummy server ကို background မှာ run ထားမယ်
    threading.Thread(target=run_dummy_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_config))
    app.run_polling()

if __name__ == "__main__":
    main()
