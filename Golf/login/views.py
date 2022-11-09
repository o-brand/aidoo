from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from .forms import RegisterForm, RegisterFormExtended
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail

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
            auth_user=form1.save(commit=False)
            auth_user.is_active=0
            user = auth_user.username
            email = auth_user.email
            auth_user.save()

            tempid = form1.save()
            userextended=form2.save(commit=False)
            userextended.user_id=tempid
            userextended.save()

            current_site = get_current_site(request)
            subject = 'Activate Your aidoo Account'
            message = render_to_string('login/account_activation_email.html', 
                {'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(auth_user.pk)),
                'token': account_activation_token.make_token(auth_user),}
                )

            send_mail(subject,message,None,[email])


            return render(request, 'login/confirm_email.html', {'email':email})

        return render(request, self.template_name, {'form1': form1, 'form2': form2})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = 1
            user.save()
            return redirect('/confirm_email/success/')
        else:
            return redirect('/confirm_email/failure/')