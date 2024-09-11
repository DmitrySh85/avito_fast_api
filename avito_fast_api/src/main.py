from fastapi import FastAPI
from message.router import router as message_router
from telegram.router import router as telegram_router


app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

app.include_router(message_router)
app.include_router(telegram_router)
