from rest_framework.exceptions import APIException

class NotFoundException(APIException):
    status_code = 404
    default_detail = "The data you looking for wasn't there."
    default_code = "data_not_found"

class ServiceError(APIException):
    status_code = 500
    default_detail = "Something went wrong here, we will get back to you soon."
    default_code = "service_error"

