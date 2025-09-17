from django.shortcuts import render, redirect
from .models import Pen, Ink
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def pen_index(request):
  pens = Pen.objects.filter(user=request.user)
  return render(request, 'pens/index.html', {'pens': pens})

@login_required
def pen_detail(request, pen_id):
  pen = Pen.objects.get(id=pen_id)
  inks = Ink.objects.all()
  return render(request, 'pens/detail.html', {
    'pen': pen,
    'inks': inks
})

class PenCreate(LoginRequiredMixin, CreateView):
  model = Pen
  fields = '__all__'

def form_valid(self, form):
  form.instance.user = self.request.user
  return super().form_valid(form)

class PenUpdate(LoginRequiredMixin, UpdateView):
  model = Pen
  fields = ['nib_size', 'nib_material', 'ink_fill', 'acquired_date', 'notes']

class PenDelete(LoginRequiredMixin, DeleteView):
    model = Pen
    success_url = '/pens/'

def associate_ink(request, pen_id, ink_id):
  Pen.objects.get(id=pen_id).inks.add(ink_id)
  return redirect('pen-detail', pen_id=pen_id)

def remove_ink(request, pen_id, ink_id):
  Pen.objects.get(id=pen_id).inks.remove(ink_id)
  return redirect('pen-detail', pen_id=pen_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pen-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)