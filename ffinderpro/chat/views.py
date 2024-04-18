from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>Football Events Forum </h1><iframe src="https://deadsimplechat.com/HAWWuE_g4" width="100%" height="600px"></iframe>')
