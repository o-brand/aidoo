from django.shortcuts import render


def redeem(request):
    # Render the page
    return render(request, "vendor/index.html", {"disabled" :"true"})
