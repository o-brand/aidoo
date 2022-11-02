from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from .forms import RegisterForm, RegisterFormExtended
from datetime import datetime

class SignUpView(View):
    form_class1 = RegisterForm
    form_class2 = RegisterFormExtended
    template_name = "login/signup.html"

    # Renders the form at the first time
    def get(self, request, *args, **kwargs):
        form1 = self.form_class1()
        form2 = self.form_class2()
        return render(request, self.template_name, {'form1': form1, 'form2': form2})

    # Processes the form after submit
    def post(self, request, *args, **kwargs):
        form1 = self.form_class1(request.POST)
        form2 = self.form_class2(request.POST)

        if form1.is_valid() and form2.is_valid():
            tempid = form1.save()
            userextended=form2.save(commit=False)
            userextended.user_id=tempid
            userextended.save()
            return redirect(reverse("login"))

        return render(request, self.template_name, {'form1': form1, 'form2': form2})
