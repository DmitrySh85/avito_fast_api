from fastapi import APIRouter, Request
from logger import logger
from .schemas import ObjectSchema
import json
from .services import send_data_to_tg


router = APIRouter(
    prefix="/api/v1/webhook",
)

@router.post("/")
async def receive_webhook(request: Request):
    payload = await request.json()
    logger.info(json.dumps(payload))
    data = ObjectSchema(**payload)
    send_data_to_tg(data)
    return {"ok": True}