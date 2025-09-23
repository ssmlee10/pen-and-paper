from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Pen, Ink, PenInkLog
from .forms import PenForm, InkForm, PenInkLogForm
from django.views.generic import ListView, DetailView
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
  pens = (Pen.objects.filter(user=request.user).order_by('brand').prefetch_related('ink_logs__ink'))
  return render(request, 'pens/index.html', {'pens': pens})

@login_required
def pen_detail(request, pen_id):
    pen = get_object_or_404(Pen, id=pen_id)
    available_inks = Ink.objects.exclude(id__in=pen.ink_logs.values_list('ink_id', flat=True))

    if request.method == "POST":
        log_form = PenInkLogForm(request.POST)
        if log_form.is_valid():
            log = log_form.save(commit=False)
            log.pen = pen
            log.save()
            return redirect("pen-detail", pen_id=pen.id)
    else:
        log_form = PenInkLogForm(initial={"pen": pen})

    return render(request, "pens/detail.html", {
        "pen": pen,
        "inks": available_inks,
        "log_form": log_form,
    })

@login_required
def mark_cleaned(request, log_id):
  log = get_object_or_404(PenInkLog, id=log_id)
  if log.date_cleaned is None:
    log.date_cleaned = timezone.now().date()
    log.save()
  return redirect("pen-detail", pen_id=log.pen.id)

class PenCreate(LoginRequiredMixin, CreateView):
  model = Pen
  form_class = PenForm

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PenUpdate(LoginRequiredMixin, UpdateView):
  model = Pen
  form_class = PenForm

class PenDelete(LoginRequiredMixin, DeleteView):
  model = Pen
  success_url = '/pens/'

class InkCreate(LoginRequiredMixin, CreateView):
   model = Ink
   form_class = InkForm

   def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def ink_list(request):
  inks = Ink.objects.all().order_by("brand", "name")
  return render(request, "ink_list.html", {"ink_list": inks})
  
@login_required
def ink_detail(request, ink_id):
  ink = Ink.objects.get(id=ink_id)
  return render(request, 'main_app/ink_detail.html', {
    'ink': ink
})
   
class InkList(ListView):
   model = Ink

class InkDetail(DetailView):
   model = Ink

class InkUpdate(UpdateView):
  model = Ink
  form_class = InkForm

class InkDelete(DeleteView):
  model = Ink
  success_url = '/inks/'

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