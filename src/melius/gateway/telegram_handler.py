import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from melius.core.agent import MeliusAgent

class MeliusGateway:
    def __init__(self, token):
        self.token = token
        self.agent = MeliusAgent()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Melius Gateway Active. Send me instructions!")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        await update.message.reply_text(f"Processing: {user_input}")
        
        # This is where the AI logic would go to decide which tool to call
        # For now, let's simulate a response
        response = f"Agent processed your request: {user_input}"
        await update.message.reply_text(response)

    def run(self):
        application = ApplicationBuilder().token(self.token).build()
        
        start_handler = CommandHandler('start', self.start)
        msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message)
        
        application.add_handler(start_handler)
        application.add_handler(msg_handler)
        
        application.run_polling()
