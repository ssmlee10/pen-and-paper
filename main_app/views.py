from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# views.py

class Pen:
    def __init__(self, brand, name):
        self.brand = brand
        self.name = name

# Create a list of Cat instances
pens = [
    Pen('Lamy', 'Lamy 2000'),
    Pen('Radius', 'Marmo Bianco'),
    Pen('Pilot', 'Custom 823'),
]

def home(request):
  return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def pen_index(request):
    # Render the cats/index.html template with the cats data
    return render(request, 'pens/index.html', {'pens': pens})