from django.shortcuts import render

from django.http import HttpResponse

def listorders(request):
    return HttpResponse("orders are listed below")
