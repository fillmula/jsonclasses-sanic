from sanic.response import HTTPResponse
from json import dumps
from jsonclasses import JSONEncoder

def json(
  body,
  status=200,
  headers=None,
  content_type='application/json'
):
  return HTTPResponse(
    dumps(body, cls=JSONEncoder),
    headers=headers,
    status=status,
    content_type=content_type
  )

def data(
  body,
  status=200,
  headers=None,
  content_type='application/json'
):
  return json(
    { 'data': body },
    status=status,
    headers=headers,
    content_type=content_type
  )

def empty(
  body,
  status=200,
  headers=None,
  content_type='application/json'
):
  return json(
    {},
    status=status,
    headers=headers,
    content_type=content_type
  )
