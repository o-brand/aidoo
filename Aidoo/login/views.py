from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from .forms import RegisterForm


# Get actual user model.
User = get_user_model()


# Get the PasswordResetTokenGenerator for account activation.
account_activation_token = PasswordResetTokenGenerator()


def welcome(request):
    """Display the welcome page or redirect."""

    # If the user did no sign out last time...
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    # Render the page
    return render(request, "welcome.html")


class SignUpView(View):
    """It is used to render the sign up page."""

    form_class = RegisterForm
    template_name = "login/signup.html"

    # Renders the form at the first time
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    # Processes the form after submit
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        # Validate the form
        if form.is_valid():
            # Create a user object from the form
            auth_user = form.save(commit=False)

            # Deactivity the account
            auth_user.is_active = 0

            # Save the user to the DB
            auth_user.save()

            # Get the user's username and email
            username = auth_user.username
            email = auth_user.email

            # Create activation email
            current_site = get_current_site(request)
            subject = "Activate Your Aidoo Account"
            message = render_to_string(
                "emails/account_activation_email.html",
                {
                    "user": username,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(auth_user.pk)),
                    "token": account_activation_token.make_token(auth_user),
                },
            )

            # Send email to the user
            send_mail(subject, message, None, [email])

            # Render the confirmation page
            return render(
                request,
                "login/activation_link_sent.html",
                {"email": email}
            )

        # Render the form again
        return render(request, self.template_name, {"form": form})


def activateAccount(request, uidb64, token):
    """It is used to activate the account of a user and redirect them."""

    try:
        # Get the user id, then the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Failure
        return redirect("/activation/failure")
    else:
        # Check the token
        if account_activation_token.check_token(user, token):
            # Activate the account and save it to the DB
            user.verified = 1
            user.save()

            # Redirect
            return redirect("/activation/success")
        else:
            # Failure
            return redirect("/activation/failure")
