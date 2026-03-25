import os
import subprocess
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8255416395:AAE_xskTzY32rhq6hwNWw5qWPD3OC1xqg4o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ /generate ကိုနှိပ်ပြီး Wireguard Config ထုတ်နိုင်ပါတယ်။")

async def generate_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("Config ထုတ်ပေးနေပါတယ်။ ခဏစောင့်ပါ...")

    # Render ရဲ့ /tmp/ folder ထဲမှာ အလုပ်လုပ်ခြင်း
    work_dir = "/tmp"
    os.chdir(work_dir)

    try:
        # wgcf register and generate
        # Path ကို သေချာအောင် /usr/local/bin/wgcf လို့ သုံးထားပါတယ်
        subprocess.run(["/usr/local/bin/wgcf", "register", "--accept-tos"], check=True)
        subprocess.run(["/usr/local/bin/wgcf", "generate"], check=True)
        
        file_path = os.path.join(work_dir, "wgcf-profile.conf")
        
        # Send the file
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                await context.bot.send_document(
                    chat_id=user_id, 
                    document=file, 
                    filename=f"WARP_{user_id}.conf"
                )
            
            # Clean up files
            if os.path.exists(os.path.join(work_dir, "wgcf-account.json")):
                os.remove(os.path.join(work_dir, "wgcf-account.json"))
            os.remove(file_path)
        else:
            await update.message.reply_text("အမှားအယွင်းရှိလို့ Config ဖိုင် မထွက်လာပါဘူး။")
        
    except Exception as e:
        await update.message.reply_text(f"Error တက်သွားပါတယ်: {str(e)}")

def main():
    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_config))
    
    # Background Worker အတွက် polling နဲ့ပဲ run ပါမယ်
    app.run_polling()

if __name__ == "__main__":
    main()
