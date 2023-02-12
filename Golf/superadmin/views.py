from django.shortcuts import render


def home(request):
    # Render the page
    return render(request, "superadmin/index.html")
