import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8255416395:AAE_xskTzY32rhq6hwNWw5qWPD3OC1xqg4o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ /generate ကိုနှိပ်ပြီး Wireguard Config ထုတ်နိုင်ပါတယ်။")

async def generate_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("Config ထုတ်ပေးနေပါတယ်။ ခဏစောင့်ပါ...")

    try:
        # wgcf register and generate
        subprocess.run(["wgcf", "register", "--accept-tos"], check=True)
        subprocess.run(["wgcf", "generate"], check=True)
        
        # Send the file
        with open("wgcf-profile.conf", "rb") as file:
            await context.bot.send_document(chat_id=user_id, document=file, filename=f"WARP_{user_id}.conf")
        
        # Clean up
        os.remove("wgcf-account.json")
        os.remove("wgcf-profile.conf")
        
    except Exception as e:
        await update.message.reply_text(f"Error တက်သွားပါတယ်: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_config))
    app.run_polling()

if __name__ == "__main__":
    main()
