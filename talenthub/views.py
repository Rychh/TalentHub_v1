from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Offer, Category, Profile
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user
from django import forms


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def search(request):
    offers = Offer.objects.all()

    category = Category.objects.all()
    cname = request.GET.get("cat")
    tnames = request.GET.get("tag")
    sort = request.GET.get("sort")

    if cname:
        offers = Offer.objects.filter(category__name=cname)

    if tnames:
        tnames = tnames.split()
        offers = offers.filter(tag__name__in=tnames).distinct()

    if sort:
        if sort == "Price: from the highest":
            offers = offers.order_by('-price')

        if sort == "Price: from the lowest":
            offers = offers.order_by('price')

        if sort == "User Name: A->Z":
            offers = offers.order_by('user_profile')

        if sort == "User Name: Z->A":
            offers = offers.order_by('-user_profile')

        if sort == "Tag: from the most matching":
            offers = offers.annotate(count=Count('pk')).distinct().order_by('-count')

    context = {'offers': offers, 'category': category}
    return render(request, 'search.html', context)


@require_GET
def profile(request, username):
    profile = Profile.objects.filter(user__username=username)
    context = {'profile': profile.first()}

    return render(request, 'profile.html', context)


@require_GET
@login_required
def myProfile(request):
    currUser = get_user(request)
    profile = Profile.objects.get(user=currUser)
    context = {'profile': profile}
    return render(request, 'myProfile.html', context)


@login_required
def myOffers(request):
    currUser = get_user(request)
    offers = Offer.objects.filter(user_profile__user=currUser)
    context = {'offers': offers}
    return render(request, 'myOffers.html', context)


@login_required
def addOffer(request):
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.user_profile = Profile.objects.filter(user=get_user(request)).first()
            post.save()
    else:
        form = OfferForm()
    return render(request, 'addOffer.html', {'form': form})

class OfferForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = ("description", "price", "category", "tag")
