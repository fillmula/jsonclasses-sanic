from traceback import extract_tb
from os import getcwd, path
import traceback
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import SanicException
from jsonclasses.exceptions import ObjectNotFoundException, ValidationException


class UnsupportedMediaTypeException(Exception):

    def __init__(self, content_type: str):
        self.message = f'Content-Type \'{content_type}\' is not supported.'
        super().__init__(self.message)


class NotAcceptableException(Exception):

    def __init__(self, accept: str):
        self.message = f'Accept \'{accept}\' is not supported.'
        super().__init__(self.message)


def remove_none(obj: dict) -> dict:
    return {k: v for k, v in obj.items() if v is not None}


def exception_handler(request: Request, exception: Exception):
    code = exception.status_code if isinstance(
        exception, SanicException) else 500
    code = 415 if isinstance(
        exception, UnsupportedMediaTypeException) else code
    code = 406 if isinstance(exception, NotAcceptableException) else code
    code = 404 if isinstance(exception, ObjectNotFoundException) else code
    code = 400 if isinstance(exception, ValidationException) else code
    if request.app.debug:
        if code == 500:
            traceback.print_last()
            return json({
                'error': remove_none({
                    'type': 'Internal Server Error',
                    'message': 'There is an internal server error.',
                    'error_type': exception.__class__.__name__,
                    'error_message': str(exception),
                    'fields': (exception.keypath_messages
                            if isinstance(exception, ValidationException)
                            else None),
                    'traceback': [f'file {path.relpath(f.filename, getcwd())}:{f.lineno} in {f.name}' for f in extract_tb(exception.__traceback__)],  # noqa: E501
                })
            }, status=code)
        else:
            return json({
                'error': remove_none({
                    'type': exception.__class__.__name__,
                    'message': str(exception),
                    'fields': (exception.keypath_messages
                            if isinstance(exception, ValidationException)
                            else None),
                    'traceback': [f'file {path.relpath(f.filename, getcwd())}:{f.lineno} in {f.name}' for f in extract_tb(exception.__traceback__)],  # noqa: E501
                })
            }, status=code)
    else:
        if code == 500:
            traceback.print_last()
            return json({
                'error': remove_none({
                    'type': 'Internal Server Error',
                    'message': 'There is an internal server error.'
                })
            }, status=500)
        else:
            return json({
                'type': exception.__class__.__name__,
                'message': str(exception),
                'fields': (exception.keypath_messages
                        if isinstance(exception, ValidationException)
                        else None)
            }, status=code)
