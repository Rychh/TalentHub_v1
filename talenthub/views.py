from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
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

    if sort:
        if sort == "Price: from the highest":
            offers = offers.order_by('-price')
        
        if sort == "Price: from the lowest":
            offers = offers.order_by('price')

        if sort == "User Name: A->Z":
            offers = offers.order_by('user_profile')

        if sort == "User Name: A->Z":
            offers = offers.order_by('-user_profile')
        
        if sort == "Tag: from the most matching":
            offers = offers.annotate(count=Count('pk')).distinct().order_by('count')

    context = { 'offers': offers, 'category':category }
    return render(request, 'search.html', context)