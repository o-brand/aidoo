from django.http import HttpResponseRedirect


# These are the urls which are available (even) if the user is NOT
# authenticated.
ENABLED_URLS = (
    "",
    "login",
    "signup",
    "logout",
    "account_activation_email",
    "help",
    "help/privacy",
    "help/community-guidelines",
    "help/manual",
)


class LoginRequiredMiddleware:
    """It is used to check if the user is authenticated."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """This function is called when communication starts with Django."""
        response = self.get_response(request)

        # If this is an error page...
        if (
            response.status_code == 404 # HttpResponseNotFound
            or response.status_code == 400 # HttpResponseBadRequest
            or response.status_code == 403 # HttpResponseForbidden
            or response.status_code == 500 # HttpResponseServerError
        ):
            return response

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            path = request.path_info.lstrip("/")

            # Is it the welcome page?
            if len(path) > 0 and path[-1] == "/":
                path = path[0:-1]

            # Is the url enabled or starts with enabled part?
            if (
                path in ENABLED_URLS
                or path.startswith("admin")
                or path.startswith("password_reset")
                or path.startswith("activate")
                or path.startswith("activation")
            ):
                return response

            # Redirect to the login page (but after login the user is
            # redirected to the requested page)
            return HttpResponseRedirect("/login?next=/" + path)

        # The user can see this page
        return response
