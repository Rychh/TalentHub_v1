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
from django.db.models.fields import IntegerField


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
    profile = Profile.objects.filter(user__username=username).first()
    opinions = Review.objects.filter(reviewed__user=profile.user).order_by('category')
    context = {'profile': profile, 'opinions': opinions}
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
            cancelMeeting(Meeting.objects.filter(pk=request.POST["deleteMeeting"]).first())

    currUser = get_user(request)
    now = timezone.now()
    updateUserMeetings(currUser)
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
def addOpinion(request, meeting_id):
    if request.method == 'POST':
        meeting = Meeting.objects.filter(id=meeting_id).first()
        meeting.status = MeetingStatus.objects.filter(name="reviewed").first()
        meeting.save()
        form = ReviewForm(request.POST)
        author = Profile.objects.filter(user=get_user(request)).first()
        rev = meeting.teacher
        cat = meeting.offer.category

        if form.is_valid():
            review = Review(
                author=author,
                reviewed=rev,
                category=cat,
                rating=form.cleaned_data['rating'],
                description=form.cleaned_data['description']
                )
            review.save()
            return redirect("myMeetings")
        else:
            return render(request, 'addOpinion.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'addOpinion.html', {'form': form})


@login_required
def addArgument(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    author = Profile.objects.filter(user=get_user(request)).first()

    number_of_arguments = Argument.objects.filter(meeting=meeting_id).count()

    if meeting.student.id != author.id or number_of_arguments > 0:
        return redirect("myArguments")

    if request.method == 'POST':
        meeting.status = MeetingStatus.objects.filter(name="reviewed").first()
        meeting.save()
        form = ArgumentForm(request.POST)

        if form.is_valid():
            argument = Argument(
                victim=author,
                accusesed = meeting.teacher,
                meeting=meeting,
                status = ArgumentStatus.objects.filter(name="pending").first(),
                message=form.cleaned_data['message'],
                )
            argument.save()
        return redirect("myArguments")
    else:
        form = ArgumentForm()
        return render(request, 'addArgument.html', {'form': form})



@login_required
def myOpinions(request):
    currUser = get_user(request)
    reviewsAsReviewed = Review.objects.filter(reviewed__user=currUser).order_by('category')
    reviewsAsAuthor= Review.objects.filter(author__user=currUser).order_by('category')

    context = {'reviewsAsReviewed': reviewsAsReviewed, 'reviewsAsAuthor': reviewsAsAuthor}
    return render(request, 'myOpinions.html', context)

@login_required
def myArguments(request):
    currUser = get_user(request)
    arguments = Argument.objects.filter(victim__user=currUser).order_by('status')
    context = {'arguments': arguments}
    return render(request, 'myArguments.html', context)



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


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ("rating", "description")

class ArgumentForm(forms.ModelForm):

    class Meta:
        model = Argument
        fields = ("message",)

