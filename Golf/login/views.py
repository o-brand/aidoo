from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from .forms import RegisterForm

class SignUpView(View):
    form_class = RegisterForm
    template_name = "login/signup.html"

    # Renders the form at the first time
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # Processes the form after submit
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("login"))

        return render(request, self.template_name, {'form': form})
