from django.shortcuts import render


def obeme(request):
    return render(request, "base.html")