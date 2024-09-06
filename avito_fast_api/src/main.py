from fastapi import FastAPI
from message.router import router as message_router


app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

app.include_router(message_router)