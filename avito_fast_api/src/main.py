from fastapi import FastAPI
from message.router import router as message_router
from telegram.router import router as telegram_router
from chat.router import router as chat_router


app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

app.include_router(message_router)
app.include_router(telegram_router)
app.include_router(chat_router)
