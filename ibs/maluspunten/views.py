from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from ibs.users.models import User
from ibs.maluspunten.models import Maluspunt
from ibs.maluspunten.form import MaluspuntForm

def index(request):
  
  if request.method == 'POST':
    form = MaluspuntForm(request.POST)
    
    if form.is_valid():

      feut = get_object_or_404(User, pk=form.cleaned_data['user'])
      added_by = get_object_or_404(User, pk=form.cleaned_data['added_by'])
      
      Maluspunt.objects.create(
        user=feut,
        added_by=added_by,
        amount=form.cleaned_data['amount'],
        reason=form.cleaned_data['reason']
      )
      
      return HttpResponseRedirect('/maluspunten/gelukt/')

  else:
    form = MaluspuntForm(initial={'added_by': request.user.id})
      
    return render(request, 'index.html', {
      'form': form,
      'user': request.user,
    })
    
    
def success(request):
  return render(request, 'success.html')


def overview(request):
  maluspunten = Maluspunt.objects.all()
  
  return render(request, 'overview.html', {
    'maluspunten': maluspunten
  })