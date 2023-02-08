from django.shortcuts import render


def home(request):
    # Render the page
    return render(request, "store/index.html")
