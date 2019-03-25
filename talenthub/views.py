from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Offer, Category

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def search(request):
    offers = Offer.objects.all()
    
    category = Category.objects.all()
    cname = request.GET.get("c")
    # cat = Category.objects.get(name__icontains = 'Maths')
    # offers = Offer.objects.filter(category = cat)
    if cname:
        cat = Category.objects.get(name__icontains = cname)
        offers = Offer.objects.filter(category = cat)
    context = { 'offers': offers, 'category':category }
    return render(request, 'search.html', context)