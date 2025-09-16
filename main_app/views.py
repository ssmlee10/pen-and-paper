from django.shortcuts import render
from .models import Pen

# Create your views here.
# views.py

def home(request):
  return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def pen_index(request):
    pens = Pen.objects.all()
    return render(request, 'pens/index.html', {'pens': pens})