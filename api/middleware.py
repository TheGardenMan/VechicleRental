import json

from api.errors import APIError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse


class ErrorHandlerMiddleware:
    """
    Custom error handler. This is set in settings.py's MIDDLEWARE list
        https://www.shubhamdipt.com/blog/django-catch-exceptions-and-custom-error-handling/
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # https://docs.djangoproject.com/en/4.0/topics/http/middleware/#process-exception
    def process_exception(self, request, exception):
        if isinstance(exception, APIError):
            # You can only return a HttpResponse from here
            return HttpResponse(
                json.dumps({"message": exception.message}),
                content_type="application/json",
                status=exception.status,
            )
        if isinstance(exception, ObjectDoesNotExist):
            return HttpResponse(
                json.dumps({"message": "Incorrect data"}),
                content_type="application/json",
                status=400,
            )
