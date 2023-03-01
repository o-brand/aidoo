from django.urls import path
from django.views.generic.base import TemplateView


# Be aware that the url already includes "help/"
urlpatterns = [
    # Landing help page
    path(
        route="",
        view=TemplateView.as_view(template_name="help/index.html"),
        name="help",
    ),
    # Privacy Policy page
    path(
        route="privacy",
        view=TemplateView.as_view(template_name="help/privacy.html"),
        name="privacy",
    ),
    # Community guidelines page
    path(
        route="community-guidelines",
        view=TemplateView.as_view(template_name="help/community-guidelines.html"),
        name="community-guidelines",
    ),
    # User manual page
    path(
        route="manual",
        view=TemplateView.as_view(template_name="help/manual.html"),
        name="manual",
    ),
]
