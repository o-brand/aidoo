from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated:
            path = request.path_info

            if path == "/" or path == "/login/" or path.startswith("/admin"):
                return self.get_response(request)

            return HttpResponseRedirect("/login/")
