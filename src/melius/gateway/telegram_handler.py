import asyncio
import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from melius.core.agent import MeliusAgent
from rich.console import Console

console = Console()

class MeliusGateway:
    def __init__(self, token, allowed_user_id=None):
        self.token = token
        self.allowed_user_id = allowed_user_id
        self.agent = MeliusAgent()
        self.config_path = os.path.expanduser("~/.melius/telegram_config.json")
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.token = config.get("token", self.token)
                self.allowed_user_id = config.get("allowed_user_id", self.allowed_user_id)

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({
                "token": self.token,
                "allowed_user_id": self.allowed_user_id
            }, f, indent=4)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if self.allowed_user_id and user.id != self.allowed_user_id:
            await update.message.reply_text("Unauthorized access. This agent is private.")
            return

        keyboard = [['/status', '/workspace'], ['/help', '/stop_gateway']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            f"Hi {user.first_name}! Melius Gateway is active and ready for your commands.",
            reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.allowed_user_id and update.effective_user.id != self.allowed_user_id:
            return

        user_text = update.message.text
        await update.message.reply_text("🤖 Melius is thinking...")
        
        # Execute agent cycle
        try:
            response = self.agent.run_cycle(user_text)
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ Melius is online and monitoring the workspace.")

    async def workspace(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        files = os.listdir(self.agent.workspace_dir)
        file_list = "\n".join([f"📄 {f}" for f in files]) or "Workspace is empty."
        await update.message.reply_text(f"Current Workspace Files:\n{file_list}")

    def run(self):
        if not self.token:
            console.print("[red]Error: Telegram token not configured. Use 'melius connect' first.[/red]")
            return

        application = ApplicationBuilder().token(self.token).build()
        
        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CommandHandler('status', self.status))
        application.add_handler(CommandHandler('workspace', self.workspace))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        
        console.print(f"[bold green]Melius Gateway started.[/bold green] Monitoring Telegram...")
        application.run_polling()
