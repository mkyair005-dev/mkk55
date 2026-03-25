import os
import subprocess
import logging
import http.server
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8255416395:AAE_xskTzY32rhq6hwNWw5qWPD3OC1xqg4o"

# Render ရဲ့ Port Error ကို ကျော်ဖို့ Dummy Server ဖွင့်ခြင်း
def run_dummy_server():
    # Render က ပေးတဲ့ PORT (Default 10000) ကို သုံးရပါမယ်
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    print(f"Server is listening on port {port}...")
    httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ /generate ကိုနှိပ်ပြီး Wireguard Config ထုတ်နိုင်ပါတယ်။")

async def generate_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("Config ထုတ်ပေးနေပါတယ်။ ခဏစောင့်ပါ...")

    # Render ရဲ့ /tmp/ folder ထဲမှာ အလုပ်လုပ်ခြင်း
    os.chdir("/tmp")

    try:
        # wgcf register and generate
        subprocess.run(["/usr/local/bin/wgcf", "register", "--accept-tos"], check=True)
        subprocess.run(["/usr/local/bin/wgcf", "generate"], check=True)
        
        file_path = "/tmp/wgcf-profile.conf"
        
        # Send the file
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                await context.bot.send_document(
                    chat_id=user_id, 
                    document=file, 
                    filename=f"WARP_{user_id}.conf"
                )
            
            # Clean up files
            if os.path.exists("/tmp/wgcf-account.json"):
                os.remove("/tmp/wgcf-account.json")
            os.remove(file_path)
        else:
            await update.message.reply_text("အမှားအယွင်းရှိလို့ Config ဖိုင် မထွက်လာပါဘူး။")
        
    except Exception as e:
        await update.message.reply_text(f"Error တက်သွားပါတယ်: {str(e)}")

def main():
    # Dummy server ကို background မှာ run ထားမှ Render က Error မပြမှာပါ
    threading.Thread(target=run_dummy_server, daemon=True).start()

    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_config))
    app.run_polling()

if __name__ == "__main__":
    main()
