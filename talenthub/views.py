from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import *
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user
from django import forms
import sys
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils import timezone


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
            offers = offers.order_by('-user_profile')

        if sort == "User Name: Z->A":
            offers = offers.order_by('user_profile')

        if sort == "Tag: from the most matching":
            offers = offers.annotate(count=Count('pk')).distinct().order_by('-count')

    context = {'offers': offers, 'category': category}
    return render(request, 'search.html', context)

@require_GET
@login_required
def profile(request, username):
    profile = Profile.objects.filter(user__username=username)
    reviews = Review.objects.filter(reviewed=profile.first()).order_by('category')
    context = {'profile': profile.first(), 'reviews': reviews}
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
def myMeetings(request):
    if request.method == "POST":
        if request.POST.get("acceptMeeting", "") != "":
            accept = MeetingStatus.objects.filter(name="agreed").first()
            Meeting.objects.filter(pk=request.POST["acceptMeeting"]).update(status=accept)
            meeting = Meeting.objects.filter(pk=request.POST.get("acceptMeeting", "")).first()

            if meeting.student.user.email != '':
                title = 'Your meeting has been accepted'
                body = 'Your meeting with ' + meeting.teacher.user.username + \
                ' on ' + str(meeting.date) + ' has been accepted. Make sure to be on time!'
                email = EmailMessage(title, body, to=[meeting.student.user.email])
                email.send()

        elif request.POST.get("deleteMeeting", "") != "":
            meeting = Meeting.objects.filter(pk=request.POST["deleteMeeting"]).first()
            meeting.student.balance += meeting.agreed_price
            meeting.student.save()  
            meeting.delete()

    currUser = get_user(request)
    now = timezone.now()
    studentHistory = Meeting.objects.filter(date__lt=now, student__user=currUser).order_by('status')
    teacherHistory = Meeting.objects.filter(date__lt=now, teacher__user=currUser).order_by('status')
    studentFuture = Meeting.objects.filter(date__gte=now, student__user=currUser).order_by('status')
    teacherFuture = Meeting.objects.filter(date__gte=now, teacher__user=currUser).order_by('status')
    context = {
        'studentHistory': studentHistory,
        'teacherHistory': teacherHistory,
        'studentFuture': studentFuture,
        'teacherFuture': teacherFuture
    }
    return render(request, 'myMeetings.html', context)


@login_required
def addOffer(request):
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.user_profile = Profile.objects.filter(user=get_user(request)).first()
            post.save()
            form.save_m2m()
    else:
        form = OfferForm()
    return render(request, 'addOffer.html', {'form': form})


@login_required
def addMeeting(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    if request.method == 'GET':
        form = MeetingForm()
        return render(request, 'addMeeting.html', {'offer': offer, 'form': form})
    elif request.method == 'POST':
        if request.user.id == offer.user_profile.user.id or request.user.profile.balance < offer.price:
            return HttpResponse("Nice try")

        form = MeetingForm(request.POST)

        if form.is_valid():
            meeting_status, created = MeetingStatus.objects.get_or_create(name = 'pending')
            meeting = Meeting(
                date = form.cleaned_data['date'],
                student = request.user.profile,
                teacher = offer.user_profile,
                offer = offer,
                agreed_price = offer.price,
                status = meeting_status,
            )
            request.user.profile.balance -= offer.price
            request.user.profile.save()
            meeting.save()

        return redirect('myMeetings')


@login_required
def addOpinion(request):
    context = {}
    return render(request, 'addOpinion.html', context)


@login_required
def addArgument(request):
    context = {}
    return render(request, 'addArgument.html', context)


@login_required
def myOpinions(request):
    currUser = get_user(request)
    reviews = Review.objects.filter(reviewed__user=currUser).order_by('category')
    context = {'reviews': reviews}
    return render(request, 'myOpinions.html', context)


class MeetingForm(forms.ModelForm):
    date = forms.fields.SplitDateTimeField(widget=forms.widgets.SplitDateTimeWidget(
        date_attrs = {'type': 'date'},
        time_attrs = {'type': 'time'}
    ))

    class Meta:
        model = Meeting
        fields = ["date"]


class OfferForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = ("description", "price", "category", "tag")
