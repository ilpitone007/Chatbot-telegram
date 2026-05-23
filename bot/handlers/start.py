from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce il comando /start."""
    user = update.effective_user
    logger.info(f"Ricevuto /start da {user.first_name} ({user.id})")

    welcome_text = (
        f"Ciao {user.first_name}! Benvenuto su AnonChat.\n\n"
        "Questo bot ti permette di chattare in completo anonimato con altri utenti.\n"
        "Usa /cerca per trovare qualcuno con cui parlare!"
    )

    await update.message.reply_text(welcome_text)
