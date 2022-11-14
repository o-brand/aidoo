from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from .forms import RegisterForm
from datetime import datetime, date
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model
account_activation_token = PasswordResetTokenGenerator()

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

        #dob_string = form['date_of_birth'].value()

        #dob = datetime.strptime(dob_string, '%Y-%m-%d').date()
        
        #years = date.today().year

        #dobmin = date.today().replace(year=years-100)
        #dobmax = date.today().replace(year=years-13)


        if form.is_valid():
            auth_user=form.save(commit=False)
            auth_user.is_active=0
            user = auth_user.username
            email = auth_user.email
            auth_user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your aidoo Account'
            message = render_to_string('login/account_activation_email.html', 
                {'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(auth_user.pk)),
                'token': account_activation_token.make_token(auth_user),}
                )

            #send_mail(subject,message,None,[email])


            return render(request, 'login/confirm_email.html', {'email':email})

        return render(request, self.template_name, {'form': form})

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