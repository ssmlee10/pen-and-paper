from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Pen
from django.contrib.auth.views import LoginView

# Create your views here.
# views.py

def home(request):
  return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def pen_index(request):
    pens = Pen.objects.all()
    return render(request, 'pens/index.html', {'pens': pens})

def pen_detail(request, pen_id):
   pen = Pen.objects.get(id=pen_id)
   return render(request, 'pens/detail.html', {'pen': pen})

class PenCreate(CreateView):
    model = Pen
    fields = '__all__'

class PenUpdate(UpdateView):
    model = Pen
    fields = ['nib_size', 'nib_material', 'ink_fill', 'acquired_date', 'notes']

class PenDelete(DeleteView):
    model = Pen
    success_url = '/pens/'

class Home(LoginView):
    template_name = 'home.html'