from sanic.request import Request
from sanic.exceptions import SanicException
from jsonclasses.exceptions import ObjectNotFoundException, ValidationException
from sanic.response import json

async def exception_handler(request: Request, exception: Exception):
  code = exception.status_code if isinstance(exception, SanicException) else 500
  code = 404 if isinstance(exception, ObjectNotFoundException) else code
  code = 400 if isinstance(exception, ValidationException) else code
  return json({
    'error': {
      'type': exception.__class__.__name__,
      'message': exception.message if hasattr(exception, 'message') else repr(exception)
    }
  }, status=code)
