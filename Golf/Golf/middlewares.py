from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

ENABLED_URLS = ("", "login/", "logout/", "update_server/")

class LoginRequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')

            if path in ENABLED_URLS or path.startswith("/admin"):
                return self.get_response(request)

            return HttpResponseRedirect("/login/")
