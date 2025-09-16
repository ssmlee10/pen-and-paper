from django.shortcuts import render, redirect
from .models import Pen
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# views.py

class Home(LoginView):
  template_name = 'home.html'

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

def form_valid(self, form):
  form.instance.user = self.request.user
  return super().form_valid(form)

class PenUpdate(UpdateView):
  model = Pen
  fields = ['nib_size', 'nib_material', 'ink_fill', 'acquired_date', 'notes']

class PenDelete(DeleteView):
    model = Pen
    success_url = '/pens/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('cat-index')
    else:
        error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)