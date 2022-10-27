from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound

def userdetail(request, user_id):
    template = loader.get_template('userprofile/profile.html')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))
