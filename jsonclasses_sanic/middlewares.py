from sanic.request import Request
from .exceptions import UnsupportedMediaTypeException, NotAcceptableException

def only_accept_middleware(content_types):
  if type(content_types) is str:
    content_types = [content_types]
  async def only_accept_content_types(request: Request):
    if request.method in ['POST', 'PATCH', 'PUT']:
      content_type = request.headers['content-type']
      for supported_content_type in content_types:
        if content_type.startswith(supported_content_type):
          return
      raise UnsupportedMediaTypeException(content_type)
  return only_accept_content_types

only_accept_json_middleware = only_accept_middleware('application/json')

def only_respond_middleware(content_types):
  if type(content_types) is str:
    content_types = [content_types]
  async def only_respond_content_types(request: Request):
    accept = request.headers['accept']
    if accept is None:
      return
    if '*/*' in accept:
      return
    for content_type in content_types:
      if content_type in accept:
        return
    raise NotAcceptableException(accept)
  return only_respond_content_types

only_respond_json_middleware = only_respond_middleware('application/json')

def only_handle_middleware(content_types):
  async def only_handle_content_types(request: Request):
    await only_accept_middleware(content_types)(request)
    await only_respond_middleware(content_types)(request)
  return only_handle_content_types

only_handle_json_middleware = only_handle_middleware('application/json')
