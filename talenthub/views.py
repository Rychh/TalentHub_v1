from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Offer, Category, Tag

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def search(request):
    offers = Offer.objects.all()
    
    category = Category.objects.all()
    cname = request.GET.get("c")
    tnames = request.GET.get("t")
    sort = request.GET.get("sort")

    if cname:
        offers = Offer.objects.filter(category__name = cname)

    if tnames:
        tnames = tnames.split()
        offers = offers.filter(tag__name__in = tnames).distinct()
                
    context = { 'offers': offers, 'category':category }
    return render(request, 'search.html', context)