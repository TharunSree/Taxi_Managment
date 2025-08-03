from .local_user import set_current_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the user for the entire duration of the request
        set_current_user(getattr(request, 'user', None))

        try:
            # Process the request
            response = self.get_response(request)
        finally:
            # Clean up the user after the request is finished
            set_current_user(None)

        return response