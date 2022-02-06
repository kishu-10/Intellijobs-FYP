from rest_framework.exceptions import APIException


class ResourceNotFoundException(APIException):
    status_code = 404
    default_detail = "The Requested Resource is not available"
    default_code = "not_available"
