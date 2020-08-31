from sanic.request import Request
from .exceptions import UnsupportedMediaTypeException, NotAcceptableException

async def accept_only_json(request: Request):
  if request.method in ['POST', 'PATCH', 'PUT']:
    content_type = request.headers['content-type']
    if content_type != 'application/json':
      raise UnsupportedMediaTypeException(content_type)

async def respond_only_json(request: Request):
  accept = request.headers['accept']
  if accept is not None:
    if '*/*' not in accept and 'application/json' not in accept:
      raise NotAcceptableException(accept)
