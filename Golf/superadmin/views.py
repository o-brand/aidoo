from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import get_user_model
from .forms import ReportForm


def home(request):
    # Render the page
    return render(request, "superadmin/index.html")

class ReportFormView(View):
    """Displays form to report a job post"""

    form_class = ReportForm
    template_name = "postreport.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {"form": form, "reporting_user": request.user.id}
        )
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return HttpResponse(status=204)
        return render(
            request, self.template_name, {"form": form, "reporting_user": request.user.id}
        )
