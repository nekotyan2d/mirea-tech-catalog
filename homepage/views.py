from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    return render(request, "404.html", status=404)


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "homepage/index.html")
