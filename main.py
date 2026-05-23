import asyncio
import logging
from config import config
from database.engine import engine
from database.models import Base
from fastapi import FastAPI
import uvicorn
from telegram.ext import ApplicationBuilder

# Setup log base
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Minimal FastAPI dashboard
app = FastAPI(title="AnonChat Dashboard")

@app.get("/")
async def root():
    return {"status": "ok", "message": "AnonChat Admin Dashboard"}

async def init_db():
    async with engine.begin() as conn:
        # Crea tutte le tabelle (solo per sviluppo/dimostrazione, in prod usa alembic)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database inizializzato.")

async def start_bot():
    if not config.bot_token or config.bot_token == "your_telegram_bot_token":
        logger.warning("Bot token non configurato. Il bot non verrà avviato.")
        return

    application = ApplicationBuilder().token(config.bot_token).build()

    logger.info("Avvio bot in modalità polling...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    # Mantiene il bot in background

async def main():
    await init_db()

    # Avvia il bot asincronamente
    asyncio.create_task(start_bot())

    # Configura e avvia uvicorn
    uvconfig = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=config.bot_port,
        log_level="info",
        reload=False
    )
    server = uvicorn.Server(uvconfig)
    logger.info(f"Avvio server ASGI su porta {config.bot_port}")
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Chiusura dell'applicazione.")
