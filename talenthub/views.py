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
    tname = request.GET.get("t")
    # cat = Category.objects.get(name__icontains = 'Maths')
    # offers = Offer.objects.filter(category = cat)
    if cname:
        # cat = Category.objects.get(name__icontains = cname) # czy oaby na pewno iconstains
        offers = Offer.objects.filter(category__name = cname)
    if tname:
        tnames = tname.split()
        # tags = Tag.objects.filter(name__iconstains=tagsname) # czy oaby na pewno iconstains
        offers = offers.filter(tag__name__in = tnames).distinct()
    context = { 'offers': offers, 'category':category }
    return render(request, 'search.html', context)