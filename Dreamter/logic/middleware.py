from django.http import Http404

def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if request.path.startswith("/admin") and request.META["SERVER_PORT"] != "5100":
            raise Http404

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
