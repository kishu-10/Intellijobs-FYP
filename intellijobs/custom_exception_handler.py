from django.http import Http404
from rest_framework.views import exception_handler

from intellijobs.exceptions.exceptions import ResourceNotFoundException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if isinstance(exc, ResourceNotFoundException):
        json_response = {
            "detail": "Resource is not available"
        }
        response.data['response'] = json_response
    if isinstance(exc, Http404):
        json_response = {
            "detail": "Resource is not available"
        }
        response.data['response'] = json_response
    return response
