from django.contrib.auth.context_processors import PermWrapper


def auth(request):
    """
    Return context variables required by apps that use Django's authentication
    system.
    """
    if hasattr(request, "user"):
        me = request.user
    else:
        from django.contrib.auth.models import AnonymousUser

        me = AnonymousUser()

    return {"me": me}
