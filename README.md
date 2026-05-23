# 📋 AnonChat Bot Telegram

**Versione:** 2.0.0
**Lingue supportate:** Italiano, Inglese
**Linguaggio:** Python 3.11+

## Panoramica del Progetto

AnonChat è un bot Telegram che permette agli utenti di avviare conversazioni anonime con sconosciuti tramite un profilo pseudonimo pre-impostato. Il sistema è progettato con un approccio **privacy by design**, offrendo disconnessione automatica a tempo, moderazione tramite blacklist e segnalazioni utenti, sistema referral a punti con scadenza, un pannello admin web real-time e un'architettura Python modulare, facilmente deployabile su VPS singola con Docker.

## Funzionalità Core

*   **Matchmaking Anonimo**: Gli utenti vengono abbinati tramite una coda (`asyncio.Queue`) con un sistema anti-loop che impedisce di incontrare la stessa persona entro 24 ore. I messaggi vengono inoltrati senza mai esporre il mittente.
*   **Onboarding e Profilo**: Configurazione in 5 step per lingua, genere, nome fittizio (da lista), età e hobby.
*   **Sistema Referral e Punti**: Punti per aver completato sessioni, valutazioni o invitato amici (con link referral a termine). Classifiche e livelli.
*   **Privacy Integrata**: Hashing degli ID Telegram tramite HMAC-SHA256, rimozione di metadati (EXIF) dalle foto e re-encoding dei vocali. Nessun salvataggio in chiaro.
*   **Moderazione e Sicurezza**: Blacklist real-time che avvisa o blocca i messaggi contenenti parole vietate. Sistema di segnalazioni in-chat gestibile tramite dashboard.
*   **Disconnessione Automatica**: Timeout per inattività (15 minuti) o limite di tempo della sessione basato sul livello utente.

## Stack Tecnologico

*   **Linguaggio**: Python 3.11+
*   **Telegram API**: `python-telegram-bot` v21+
*   **Database**: SQLite + `aiosqlite`
*   **ORM e Migrazioni**: SQLAlchemy 2.0 + Alembic
*   **Dashboard Admin Web**: FastAPI, Uvicorn, Jinja2, Chart.js
*   **Scheduler**: APScheduler 3.x (AsyncIOScheduler)
*   **Deploy**: Docker, docker-compose, Nginx (Reverse Proxy)
*   **Testing**: `pytest`, `pytest-asyncio`

## Configurazione

Crea un file `.env` e configura le variabili necessarie.

```env
# Bot Telegram
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_URL=https://yourdomain.com   # Vuoto per polling
WEBHOOK_SECRET=random_secret_string
BOT_PORT=8443

# Sicurezza
SECRET_KEY=your_hmac_secret_key_min_32_chars

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/anonchat.db

# Admin Dashboard
ADMIN_USERNAME=admin
ADMIN_PASSWORD=strong_password_here
ADMIN_IP_WHITELIST=1.2.3.4,5.6.7.8   # Vuoto per nessuna restrizione

# Configurazione sessioni, punti e referral (vedi default)
```

## Installazione e Deploy (Docker)

L'applicazione è progettata per essere servita facilmente tramite Docker Compose, che orchestra il backend Python (Bot + FastAPI) e il reverse proxy Nginx.

```bash
# 1. Clona la repository
git clone https://github.com/.../anonchat.git
cd anonchat

# 2. Configura le variabili d'ambiente
cp .env.example .env
nano .env

# 3. Avvia il container tramite Docker Compose
docker-compose up -d --build
```

### Struttura Architetturale

Il progetto segue una struttura a moduli indipendenti:

*   `bot/`: Handler, middleware e tastiere per l'interazione con Telegram.
*   `core/`: Logica del bot come matchmaking, session relay, timeout manager e anonymizer.
*   `dashboard/`: Applicazione web FastAPI per la gestione amministrativa.
*   `database/`: Modelli SQLAlchemy, migrazioni Alembic e setup del DB.
*   `services/`: Servizi applicativi per utenza, punti, report, etc.
*   `utils/`, `i18n/`, `scripts/`: Strumenti accessori per internazionalizzazione, logging, script asincroni (es. validazioni, EXIF cleaner).

## Testing

Per eseguire la test suite (copertura minima richiesta: 80%):
```bash
pytest tests/ --asyncio-mode=auto --cov=anonchat --cov-report=term-missing
```

---
*Nota: Questa applicazione raccoglie informazioni ed elabora messaggi sensibili; seguire scrupolosamente i prerequisiti di sicurezza (DPIA, GDPR, conformità locale) prima del lancio.*