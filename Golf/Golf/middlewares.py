from django.http import HttpResponseRedirect

ENABLED_URLS = ("", "login", "signup", "logout", "update_server")

class LoginRequiredMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')

            if len(path) > 0 and path[-1] == '/':
                path = path[0:-1]

            if path in ENABLED_URLS or path.startswith("admin") or path.startswith("password_reset"):
                return response

            return HttpResponseRedirect("/login/?next=/" + path)

        return response
