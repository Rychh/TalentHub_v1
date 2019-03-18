from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Offer

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def search(request):
    offers = Offer.objects.all()
    context = { 'offers': offers }
    return render(request, 'search.html', context)