from django.shortcuts import render

from . import util

from django.http import HttpResponse


def home(request):
    return HttpResponse("HI")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
