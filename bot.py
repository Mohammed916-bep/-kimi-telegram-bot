import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

async def chat_with_kimi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    
    try:
        response = await client.chat.completions.create(
            model="moonshotai/kimi-k2.5",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=1024
        )
        
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f"عذراً، حدث خطأ: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_kimi))
    app.run_polling()

if __name__ == "__main__":
    main()
