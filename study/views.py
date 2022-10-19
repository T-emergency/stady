from django.shortcuts import render, redirect
from . import webcam

# Create your views here.
def test(request):
    return render(request, 'temp.html')


