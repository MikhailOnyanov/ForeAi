from starlette.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from ..services.message_service import MessageService
from ..dependencies import logger

router = APIRouter(
    prefix="/message",
    tags=["message"]
)


@router.get('/generate_response')
def reply_user_message(message: str):
    try:
        service = MessageService()
        response_message = service.make_response(message)
        return JSONResponse(content=jsonable_encoder(response_message), status_code=200, media_type="application/json")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=f"Bad news...")
