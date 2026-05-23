# 📋 Requisiti — AnonChat Bot Telegram

> **Versione:** 2.0.0
> **Data:** Maggio 2026
> **Lingue supportate:** Italiano, Inglese
> **Piattaforma:** Telegram Bot API
> **Linguaggio:** Python 3.11+

---

## 1. Panoramica del Progetto

AnonChat è un bot Telegram che permette a utenti di avviare conversazioni anonime con sconosciuti tramite un profilo pseudonimo pre-impostato. Il sistema è progettato con **privacy by design**, disconnessione automatica a tempo, moderazione tramite blacklist e segnalazioni utenti, sistema referral a punti con scadenza, pannello admin web real-time e architettura Python modulare deployabile su VPS singola con Docker.

---

## 2. Stack Tecnologico

| Componente | Tecnologia | Motivazione |
|---|---|---|
| Linguaggio | Python 3.11+ | Tipizzazione moderna, async nativo |
| Framework bot | `python-telegram-bot` v21+ | Stabile, ottimo supporto webhook/polling |
| Database | SQLite + `aiosqlite` | Semplice, locale, zero dipendenze esterne |
| ORM | `SQLAlchemy 2.0` (async) | Migrazioni pulite, query type-safe |
| Migrazioni DB | `Alembic` | Versioning schema senza perdita dati |
| Code matchmaking | `asyncio.Queue` in-memory | Leggero, nessuna dipendenza esterna |
| Scheduler | `APScheduler 3.x` (AsyncIOScheduler) | Timeout sessioni, scadenza punti, pulizia dati |
| Web dashboard | `FastAPI` + `Jinja2` + `Chart.js` | Dashboard admin real-time |
| Server ASGI | `Uvicorn` | Serve webhook Telegram e dashboard in un unico processo |
| Deploy | Docker + `docker-compose` | Singola VPS, isolamento ambiente |
| Reverse proxy | Nginx + Let's Encrypt | SSL/TLS obbligatorio per webhook |
| Logging | `structlog` | Log strutturati JSON, mai contenuto messaggi |
| Qualità codice | `ruff` + `mypy` | Linting e type checking uniformi |
| Testing | `pytest` + `pytest-asyncio` | Unit e integration test per ogni modulo |

---

## 3. Architettura Modulare Python

Il progetto segue una struttura a **moduli indipendenti**, ognuno con responsabilità singola. Ogni modulo espone solo l'interfaccia pubblica necessaria agli altri.

```
anonchat/
│
├── main.py                        # Entry point: avvia bot + server ASGI
├── config.py                      # Configurazione da .env via pydantic-settings
│
├── database/
│   ├── __init__.py
│   ├── engine.py                  # Setup SQLAlchemy async engine (SQLite)
│   ├── models.py                  # Tutti i modelli ORM
│   └── migrations/                # Cartella Alembic
│       ├── env.py
│       └── versions/
│
├── bot/
│   ├── __init__.py
│   ├── application.py             # Setup Application PTB, registrazione handler
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py               # /start, onboarding, creazione profilo
│   │   ├── profile.py             # /profilo, modifica pseudonimo
│   │   ├── search.py              # /cerca, /annulla, gestione coda
│   │   ├── chat.py                # Relay messaggi durante sessione attiva
│   │   ├── session.py             # /fine, disconnessione volontaria
│   │   ├── referral.py            # /referral, /punti, /classifica
│   │   ├── report.py              # /segnala, gestione segnalazioni
│   │   ├── settings.py            # /impostazioni, lingua, preferenze
│   │   ├── privacy.py             # /privacy, /cancella
│   │   └── admin.py               # Comandi admin riservati (ban, stats)
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── language.py            # Rilevamento lingua IT/EN, iniezione nel context
│   │   ├── auth.py                # Controllo ban/sospensione prima di ogni handler
│   │   └── rate_limiter.py        # Rate limiting 30 msg/min per utente
│   │
│   └── keyboards/
│       ├── __init__.py
│       ├── profile_kb.py          # InlineKeyboard per onboarding step-by-step
│       ├── session_kb.py          # Bottoni durante sessione (Segnala, Fine)
│       └── menu_kb.py             # Menu principale e navigazione
│
├── core/
│   ├── __init__.py
│   ├── matchmaking.py             # asyncio.Queue, logica abbinamento, anti-loop
│   ├── session_manager.py         # Creazione/chiusura sessioni, relay messaggi
│   ├── timeout_manager.py         # APScheduler: inattività 15 min, max per livello
│   ├── anonymizer.py              # Strip EXIF foto, re-encode audio, delay randomizzato
│   └── blacklist.py               # Caricamento/hot-reload blacklist, filtro testo
│
├── services/
│   ├── __init__.py
│   ├── user_service.py            # CRUD utenti, hashing UUID, calcolo livello
│   ├── points_service.py          # Accredito punti, scadenza 12 mesi, leaderboard
│   ├── referral_service.py        # Generazione link, validazione 48h, catena 2 livelli
│   ├── report_service.py          # Salvataggio hash report, escalation automatica
│   └── moderation_service.py      # Orchestrazione blacklist + segnalazioni + ban
│
├── dashboard/
│   ├── __init__.py
│   ├── app.py                     # FastAPI app, router, autenticazione admin
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── overview.py            # Statistiche real-time + SSE
│   │   ├── users.py               # Lista utenti, dettaglio, azioni di moderazione
│   │   ├── sessions.py            # Sessioni attive e storico aggregato
│   │   ├── reports.py             # Coda segnalazioni da moderare
│   │   ├── referrals.py           # Statistiche referral
│   │   └── blacklist.py           # Gestione parole vietate con hot reload
│   ├── templates/                 # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── overview.html
│   │   ├── users.html
│   │   ├── sessions.html
│   │   ├── reports.html
│   │   ├── referrals.html
│   │   └── blacklist.html
│   └── static/
│       ├── css/
│       └── js/                    # Chart.js, aggiornamento SSE real-time
│
├── i18n/
│   ├── __init__.py
│   ├── translator.py              # Funzione t(key, lang, **kwargs)
│   ├── it.json                    # Tutti i testi in italiano
│   └── en.json                    # Tutti i testi in inglese
│
├── utils/
│   ├── __init__.py
│   ├── crypto.py                  # HMAC-SHA256, generazione UUID, token
│   ├── exif_cleaner.py            # Strip metadati immagini (Pillow)
│   ├── validators.py              # Validazione input utente
│   └── logger.py                  # Setup structlog, filtro dati sensibili
│
├── tests/
│   ├── conftest.py                # Fixture: DB in-memory, bot mock
│   ├── test_matchmaking.py
│   ├── test_session_manager.py
│   ├── test_points_service.py
│   ├── test_referral_service.py
│   ├── test_blacklist.py
│   ├── test_anonymizer.py
│   └── test_dashboard_routes.py
│
├── scripts/
│   ├── seed_blacklist.py          # Popola blacklist iniziale
│   └── expire_points.py           # Scadenza punti (eseguito da APScheduler)
│
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── alembic.ini
├── pyproject.toml
└── README.md
```

### 3.1 Principi Architetturali

**Separazione delle responsabilità:** gli `handlers/` non contengono logica di business — chiamano solo i `services/`. I `services/` non conoscono Telegram — operano solo su dati e DB. Il `core/` gestisce la logica real-time (matchmaking, relay, timeout).

**Dependency injection:** ogni service riceve la sessione DB come parametro, mai come singleton globale. Questo rende i test isolati e deterministici.

**Async-first:** tutto il codice I/O (DB, file, rete) usa `async/await`. Nessuna chiamata bloccante nel thread principale.

**Config centralizzata:** `config.py` carica tutte le variabili da `.env` tramite `pydantic-settings`. Nessuna stringa hardcoded nel codice.

**i18n by design:** nessun testo hardcoded negli handler — tutto passa per `t(key, lang)` in `i18n/translator.py`. La lingua viene rilevata dal middleware e iniettata nel context PTB ad ogni update.

**Testabilità:** ogni modulo ha interfacce chiare e mockabili. Il DB usa SQLite in-memory nei test. L'`Application` PTB è mockabile senza connessione reale a Telegram.

---

## 4. Database — Modello Dati (SQLite)

### Tabella `users`
| Campo | Tipo | Note |
|---|---|---|
| `id` | TEXT PK | UUID interno (HMAC-SHA256 del chat_id) |
| `lang` | TEXT | `it` o `en` |
| `gender` | TEXT | `male`, `female`, `nonbinary` |
| `display_name` | TEXT | Nome fittizio scelto dalla lista |
| `age_range` | TEXT | `18-24`, `25-34`, `35-44`, `45+` |
| `hobbies` | TEXT | JSON array, max 3 elementi |
| `level` | TEXT | `newbie`, `explorer`, `social`, `legend` |
| `total_points` | INTEGER | Saldo punti attuale |
| `is_banned` | BOOLEAN | Ban permanente |
| `suspended_until` | DATETIME | NULL se non sospeso |
| `warning_count` | INTEGER | Avvisi accumulati |
| `created_at` | DATETIME | |
| `last_active_at` | DATETIME | Usato per calcolo scadenza punti |

### Tabella `sessions`
| Campo | Tipo | Note |
|---|---|---|
| `id` | TEXT PK | UUID sessione |
| `user_a_id` | TEXT FK | Primo utente |
| `user_b_id` | TEXT FK | Secondo utente |
| `started_at` | DATETIME | |
| `ended_at` | DATETIME | NULL se attiva |
| `end_reason` | TEXT | `timeout_idle`, `timeout_max`, `voluntary`, `report` |
| `rating_a` | INTEGER | Valutazione da user_a (1–5) |
| `rating_b` | INTEGER | Valutazione da user_b (1–5) |
| `message_count` | INTEGER | Contatore messaggi (no contenuto) |

### Tabella `referrals`
| Campo | Tipo | Note |
|---|---|---|
| `id` | INTEGER PK | |
| `referrer_id` | TEXT FK | Chi ha invitato |
| `referred_id` | TEXT FK | Chi è stato invitato |
| `level` | INTEGER | 1 o 2 |
| `link_token` | TEXT | Token univoco del link |
| `link_expires_at` | DATETIME | +48h dalla generazione |
| `bonus_paid` | BOOLEAN | True quando il bonus è stato accreditato |
| `created_at` | DATETIME | |

### Tabella `points_log`
| Campo | Tipo | Note |
|---|---|---|
| `id` | INTEGER PK | |
| `user_id` | TEXT FK | |
| `amount` | INTEGER | Positivo o negativo |
| `reason` | TEXT | `session`, `rating`, `referral`, `referral_bonus`, `streak`, `signup` |
| `expires_at` | DATETIME | `last_active_at` + 12 mesi |
| `created_at` | DATETIME | |

### Tabella `reports`
| Campo | Tipo | Note |
|---|---|---|
| `id` | INTEGER PK | |
| `reporter_id` | TEXT FK | |
| `reported_id` | TEXT FK | |
| `session_hash` | TEXT | SHA256 di session_id (no contenuto) |
| `category` | TEXT | `offensive`, `explicit`, `spam`, `other` |
| `status` | TEXT | `pending`, `reviewed`, `dismissed` |
| `created_at` | DATETIME | |

### Tabella `blacklist`
| Campo | Tipo | Note |
|---|---|---|
| `id` | INTEGER PK | |
| `word` | TEXT UNIQUE | Parola o pattern vietato |
| `severity` | TEXT | `warn` o `block` |
| `added_by` | TEXT | Admin che l'ha aggiunta |
| `created_at` | DATETIME | |

---

## 5. Funzionalità Core

### 5.1 Onboarding e Profilo Anonimo

All'avvio (`/start`) il bot guida l'utente in 5 step sequenziali tramite menu inline:

**Step 1 — Lingua:** rilevata automaticamente da `language_code` Telegram, confermabile manualmente: 🇮🇹 Italiano / 🇬🇧 English.

**Step 2 — Genere:** 👨 Uomo / 👩 Donna / 🧑 Non binario

**Step 3 — Nome fittizio:** lista 50+ nomi per genere, presentati a blocchi di 8 con paginazione inline. Nessun input libero consentito.

**Step 4 — Fascia d'età:** 18–24 / 25–34 / 35–44 / 45+

**Step 5 — Hobby** (multi-selezione, max 3):
🎮 Videogiochi · 🎵 Musica · 📚 Lettura · 🏋️ Sport · 🎨 Arte · 🍕 Cucina · ✈️ Viaggi · 🎬 Film/Serie · 💻 Tech · 🐾 Animali · 🌿 Outdoor · 📸 Fotografia

**Completamento:** +50 PT accreditati, riepilogo profilo. Il profilo è modificabile con `/profilo` in qualsiasi momento.

### 5.2 Matchmaking

Il modulo `core/matchmaking.py` gestisce una `asyncio.Queue` per gli utenti in attesa. Abbinamento FIFO con controllo anti-loop (nessuna sessione con lo stesso partner nelle ultime 24 ore).

- Timeout coda: **60 secondi** → notifica e rimozione automatica
- `/annulla` per uscire dalla coda in qualsiasi momento
- Utenti sospesi o bannati bloccati in ingresso dal middleware `auth.py`
- Explorer+: filtro opzionale per hobby in matchmaking

### 5.3 Relay Anonimo

Il modulo `core/session_manager.py` mantiene in memoria `{user_id: partner_id}`. Ogni messaggio viene inoltrato tramite `bot.copy_message()` senza esporre il mittente.

**Messaggi supportati:** testo, emoji, sticker, GIF, foto (strip EXIF), vocali (re-encode), video brevi.

**Messaggi bloccati:** contatti, localizzazione, file (PDF, DOCX, ZIP...), sondaggi, giochi Telegram.

**Filtro blacklist real-time:** ogni testo passa per `core/blacklist.py` prima dell'inoltro. `warn` → avviso privato; `block` → messaggio bloccato + avviso. Tre hit `block` in una sessione → disconnessione + segnalazione auto-generata.

### 5.4 Disconnessione Automatica

Il modulo `core/timeout_manager.py` usa `APScheduler` con `AsyncIOScheduler`.

| Trigger | Comportamento |
|---|---|
| Inattività 15 minuti | Avviso → 60 sec per rispondere → disconnessione |
| Timeout massimo sessione | 60/90/120 min per livello, illimitato per Legend |
| `/fine` volontario | Disconnessione immediata, notifica al partner |
| Contenuto esplicito confermato | Avviso + sospensione 24h + disconnessione |
| Report approvato da admin | Disconnessione immediata |

Alla disconnessione: messaggio riepilogo + valutazione opzionale ⭐ 1–5 + +10 PT se sessione ≥ 5 minuti.

### 5.5 Comandi Bot

| Comando | Descrizione |
|---|---|
| `/start` | Avvia il bot e crea il profilo |
| `/cerca` | Entra in coda matchmaking |
| `/annulla` | Annulla la ricerca in corso |
| `/fine` | Termina la sessione attiva |
| `/profilo` | Visualizza e modifica il profilo |
| `/punti` | Saldo punti e livello attuale |
| `/referral` | Genera o visualizza il link di invito |
| `/classifica` | Top 10 settimanale |
| `/impostazioni` | Lingua, filtri, notifiche |
| `/segnala` | Segnala durante una sessione |
| `/privacy` | Informativa privacy |
| `/cancella` | Elimina tutti i dati personali |
| `/help` | Lista comandi |

---

## 6. Lingua e Internazionalizzazione

**Lingue supportate:** Italiano (default) e Inglese.

Il middleware `bot/middleware/language.py` rileva `language_code` dall'`Update` Telegram e lo salva nel profilo. Modificabile con `/impostazioni`. La funzione `t(key, lang, **kwargs)` in `i18n/translator.py` gestisce le sostituzioni dinamiche. Nessun testo hardcoded negli handler.

---

## 7. Sistema Privacy

### 7.1 Hashing Identità

```python
# utils/crypto.py
import hmac, hashlib

def hash_user_id(telegram_chat_id: int, secret_key: str) -> str:
    return hmac.new(
        secret_key.encode(),
        str(telegram_chat_id).encode(),
        hashlib.sha256
    ).hexdigest()
```

Il `chat_id` Telegram non viene mai salvato in chiaro. L'UUID è deterministico ma non reversibile senza la `SECRET_KEY`.

### 7.2 Retention Dati

| Dato | Retention |
|---|---|
| UUID + profilo pseudonimo | Fino a `/cancella` |
| Punti e log referral | Fino a `/cancella`; punti scadono dopo 12 mesi di inattività |
| Timestamp sessioni (aggregati) | 90 giorni, poi eliminati da scheduler |
| Hash report | 30 giorni |
| Blacklist hit (contatori) | Aggregati settimanali, nessuna traccia per-utente |

### 7.3 Anonimizzazione Messaggi

- `copy_message()` non include `forward_from` né `forward_origin`
- Foto: strip EXIF completo via **Pillow** in `utils/exif_cleaner.py` prima del re-invio
- Audio/vocali: re-inviati da buffer in-memory come `InputFile`, nessun file su disco
- Delay randomizzato ±150ms su ogni relay per prevenire timing attack

### 7.4 Cancellazione Dati

1. `/cancella` → conferma inline (anti-accidentale)
2. Eliminazione immediata da tutte le tabelle via `user_service.delete_user(uuid)`
3. UUID invalidato (tombstone anonimo 24h per prevenire re-registrazione immediata)
4. Messaggio di conferma con timestamp

### 7.5 Sicurezza Infrastruttura

- Server in **UE** (conformità GDPR)
- File SQLite con permessi `600`, accessibile solo dall'utente applicazione
- Nessun log di messaggi o `chat_id` in chiaro — `structlog` filtra automaticamente i campi sensibili in `utils/logger.py`
- Variabili sensibili solo via `.env`, mai nel codice
- Nginx con header: `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`
- Dashboard admin: Basic Auth + IP whitelist configurabile

---

## 8. Sistema di Referral e Punti

### 8.1 Guadagnare Punti

| Azione | Punti |
|---|---|
| Prima configurazione profilo | +50 PT |
| Sessione ≥ 5 minuti completata | +10 PT |
| Valutazione lasciata | +5 PT |
| Invitato diretto (L1) completa il profilo | +100 PT |
| Invitato diretto (L1) completa 5 sessioni | +50 PT bonus |
| Invitato di 2° livello (L2) completa il profilo | +25 PT |
| Streak 7 giorni consecutivi con sessione | +70 PT |

### 8.2 Scadenza Punti (12 mesi)

I punti scadono 12 mesi dopo `last_active_at`. Lo scheduler esegue ogni notte `scripts/expire_points.py` che invalida i record con `expires_at < now()` e ricalcola `total_points`. L'utente riceve una notifica Telegram **30 giorni prima** se inattivo.

### 8.3 Link Referral

```
https://t.me/<BotUsername>?start=ref_<token_8char>
```

Token generato con `secrets.token_urlsafe(6)`. Valido **48 ore** dalla generazione. Nuovo link invalida il precedente.

### 8.4 Livelli

| Livello | Soglia | Benefici |
|---|---|---|
| 🥉 Newbie | 0–199 PT | Base, timeout sessione 60 min |
| 🥈 Explorer | 200–599 PT | Timeout 90 min, filtro hobby in matchmaking |
| 🥇 Social | 600–1499 PT | Timeout 120 min, priorità in coda |
| 💎 Legend | 1500+ PT | Timeout illimitato, badge esclusivo nel profilo |

### 8.5 Anti-Abuso

- Hashing deterministico: stesso account → stesso UUID → impossibile registrarsi due volte
- Bonus accreditato solo dopo ≥ 1 sessione da ≥ 5 minuti dell'invitato
- Catena bloccata al 2° livello
- Più di 20 referral in 24h → flag per revisione admin

---

## 9. Moderazione

### 9.1 Blacklist Parole Vietate

`core/blacklist.py` carica la lista da DB all'avvio e la mantiene come `set` in-memory per lookup O(1). Hot reload dalla dashboard senza riavvio.

| Severità | Comportamento |
|---|---|
| `warn` | Messaggio inoltrato, avviso privato al mittente |
| `block` | Messaggio bloccato, avviso al mittente |

Tre hit `block` in una sessione → disconnessione + segnalazione auto-generata.

### 9.2 Segnalazioni Utenti

Durante una sessione, bottone **Segnala** o `/segnala` → menu categorie:
- 🤬 Linguaggio offensivo / hate speech
- 🔞 Contenuto esplicito non richiesto
- 🤖 Spam o comportamento da bot
- ❓ Altro

Salva in `reports`: hash della sessione (SHA256 di `session_id`), categoria, status `pending`. Nessun contenuto di messaggi.

### 9.3 Contenuto Esplicito

Se una segnalazione per contenuto esplicito viene approvata dall'admin:
1. Avviso Telegram all'utente (in IT o EN in base alla lingua del profilo)
2. `suspended_until = now() + 24h`
3. `warning_count += 1`
4. Disconnessione sessione attiva

### 9.4 Escalation Automatica

| Condizione | Azione |
|---|---|
| 3 segnalazioni in 7 giorni | Sospensione automatica 24h |
| 2 sospensioni in 30 giorni | Ban temporaneo 7 giorni |
| Ban temporaneo + nuova violazione | Ban permanente (richiede conferma admin) |

---

## 10. Webhook e Polling

Modalità primaria: **webhook** (richiede URL HTTPS configurato). Fallback automatico a **polling** se `WEBHOOK_URL` non è impostato nell'`.env` (utile per sviluppo locale).

```python
# bot/application.py (logica semplificata)
async def run():
    if config.WEBHOOK_URL:
        await app.run_webhook(
            listen="0.0.0.0",
            port=config.BOT_PORT,
            webhook_url=f"{config.WEBHOOK_URL}/telegram",
            secret_token=config.WEBHOOK_SECRET,
        )
    else:
        await app.run_polling(drop_pending_updates=True)
```

Nginx gestisce SSL e fa da reverse proxy verso `localhost:8443`.

---

## 11. Dashboard Admin Web (FastAPI)

Servita dallo stesso processo Uvicorn su path `/admin`. Protetta da **HTTP Basic Auth** + **IP whitelist** configurabile.

### 11.1 Sezioni

**Overview (real-time):** utenti totali, sessioni attive, messaggi relayati oggi (aggregato), nuovi utenti 24h, top 5 hobby, grafico sessioni per ora. Aggiornamento automatico via **SSE** ogni 5 secondi.

**Utenti:** tabella paginata con UUID abbreviato, livello, punti, stato. Azioni: dettaglio, sospendi, ban temporaneo, ban permanente, sblocca.

**Sessioni:** sessioni attive in tempo reale (UUID utenti, durata, messaggi). Storico aggregato 30 giorni. Nessun contenuto messaggi.

**Segnalazioni:** coda `status=pending` ordinata per data. Admin può: approvare (applica sanzione), ignorare, aggiungere nota.

**Referral:** top 20 per referral generati, tasso conversione, punti distribuiti totali.

**Blacklist:** lista parole con severità. Form aggiunta/modifica/eliminazione. Hot reload immediato nel core.

### 11.2 Aggiornamento Real-Time (SSE)

Overview e Sessioni usano **Server-Sent Events** per aggiornamento automatico ogni 5 secondi. Il server invia JSON con metriche aggiornate; `Chart.js` aggiorna i grafici client-side senza refresh.

---

## 12. Configurazione (.env)

```env
# Bot Telegram
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_URL=https://yourdomain.com   # Lasciare vuoto per polling (sviluppo)
WEBHOOK_SECRET=random_secret_string
BOT_PORT=8443

# Sicurezza
SECRET_KEY=your_hmac_secret_key_min_32_chars

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/anonchat.db

# Admin Dashboard
ADMIN_USERNAME=admin
ADMIN_PASSWORD=strong_password_here
ADMIN_IP_WHITELIST=1.2.3.4,5.6.7.8   # Vuoto = nessuna restrizione IP

# Sessioni
DEFAULT_SESSION_TIMEOUT_MINUTES=60
IDLE_TIMEOUT_MINUTES=15
QUEUE_TIMEOUT_SECONDS=60

# Referral e Punti
REFERRAL_LINK_TTL_HOURS=48
MAX_REFERRAL_PER_DAY=20
POINTS_EXPIRY_MONTHS=12

# Notifiche scadenza punti
EXPIRY_WARNING_DAYS=30
```

---

## 13. Docker e Deploy

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .
RUN alembic upgrade head

CMD ["python", "main.py"]
```

### docker-compose.yml

```yaml
services:
  anonchat:
    build: .
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./data:/app/data        # SQLite persistente
      - ./logs:/app/logs
    ports:
      - "127.0.0.1:8443:8443"  # Solo localhost, Nginx fa da proxy

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - anonchat
```

---

## 14. Testing

| File di test | Cosa copre |
|---|---|
| `test_matchmaking.py` | Abbinamento, anti-loop, timeout coda |
| `test_session_manager.py` | Apertura/chiusura sessione, relay, disconnessione |
| `test_points_service.py` | Accredito, scadenza 12 mesi, calcolo livello |
| `test_referral_service.py` | Generazione link, validazione 48h, catena L2, anti-abuso |
| `test_blacklist.py` | Filtro testo, hot reload, severità |
| `test_anonymizer.py` | Strip EXIF, re-encode audio, delay randomizzato |
| `test_dashboard_routes.py` | Autenticazione, endpoint, SSE |

Comando unico: `pytest tests/ --asyncio-mode=auto --cov=anonchat --cov-report=term-missing`
Coverage minima richiesta: **80%**.

---

## 15. Requisiti Non Funzionali

| Requisito | Target |
|---|---|
| Latenza relay messaggio | < 500ms (p99) |
| Disponibilità | 99.5% mensile |
| Sessioni simultanee | ≥ 200 (SQLite + asyncio; scalabile a PostgreSQL se necessario) |
| Tempo risposta matchmaking | < 2 secondi se utenti in coda |
| Conformità normativa | GDPR (UE 2016/679) |
| Python version | 3.11+ |
| Coverage test minima | 80% |

---

## 16. Roadmap Versioni Future

| Versione | Feature |
|---|---|
| v1.1 | Filtro matchmaking avanzato per hobby e fascia d'età (Explorer+) |
| v1.2 | Migrazione opzionale a PostgreSQL per volumi elevati |
| v1.3 | Modalità gruppo anonima (3 sconosciuti) |
| v1.4 | Badge collezionabili e profilo avanzato |
| v2.0 | Mini-app Telegram con UI grafica |

---

## 17. Note Legali e Privacy

- Informativa `/privacy` conforme **Art. 13 GDPR**, in IT e EN, linguaggio semplice.
- Eseguire **DPIA** (Data Protection Impact Assessment) prima del lancio pubblico.
- Nominare un responsabile del trattamento e documentare il registro trattamenti (Art. 30 GDPR).
- Audit di sicurezza esterno consigliato prima della produzione.
- Età minima utenti: **18 anni** — disclaimer obbligatorio al primo avvio.

---

*Documento requisiti v2.0 — soggetto a revisione iterativa durante lo sviluppo.*
