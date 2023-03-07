from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import ReportForm
from django.views.generic import ListView

from .models import ReportTicket




class ReportFormView(View):
    """Displays form to report a job post"""

    form_class = ReportForm
    template_name = "postreport.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {
                "form": form,
            }
        )
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return HttpResponse(status=204)
        
        return render(
            request, self.template_name, {"form": form, 
                "reporting_user": request.user.id,
                "reported_job": request.POST.get("job_id"),
                "reported_user":request.POST.get("user_id")},
        )

class ReportsView(ListView):
    """Displays a list to show the reports."""

    model = ReportTicket
    template_name = "superadmin/index.html"
    context_object_name = "tickets"

    def get_queryset(self):
        """Reads reports from the database."""
        me = self.request.user
        tickets = ReportTicket.objects.filter(user_id=me)

        return tickets

