import logging

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ..services.message_service import MessageService


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/message',
    tags=['message']
)

INTERNAL_SERVER_ERROR = HTTPException(
    status_code=500,
    detail={'message': 'Internal Server Error'},
)

@router.get('/generate_response')
def reply_user_message(message: str):
    try:
        logger.info(f'Received message: {message}')
        service = MessageService()
        logger.info('Initialized message service')
        response_message = service.make_response(message)
        return JSONResponse(content=jsonable_encoder(response_message), status_code=200, media_type='application/json')
    except Exception as e:
        logger.exception(e)
        raise INTERNAL_SERVER_ERROR from e
