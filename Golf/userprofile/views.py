from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def userdetail(request, user_id):
    template = loader.get_template('userprofile/profile.html')
    context = {
        'user': User.objects.get(pk=user_id),
    }
    return HttpResponse(template.render(context, request))
