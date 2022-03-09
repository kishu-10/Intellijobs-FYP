from django.urls import reverse
from django.shortcuts import redirect
from django.http import Http404


class RestrictUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # restrict dashboard to normal users

        if request.path.find("/dashboard/") > -1:
            if not request.user.is_superuser and not request.user.has_dashboard_access:
                raise Http404('No Access to the page')
        response = self.get_response(request)

        return response
