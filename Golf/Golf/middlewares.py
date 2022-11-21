from django.http import HttpResponseRedirect


# These are the urls which are available (even) if the user is NOT
# authenticated.
ENABLED_URLS = ("", "login", "signup", "logout", "privacy",
    "account_activation_email")


class LoginRequiredMiddleware:
    """It is used to check if the user is authenticated."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """This function is called when communication starts with Django."""
        response = self.get_response(request)

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
