from django.utils import timezone
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User

FIRST_NAME_LEN = 20
LAST_NAME_LEN = 20
CATEGORY_NAME_LEN = 30
OFFER_DESC_LEN = 1000
TAG_LEN = 1000
MEETING_STATUS_LEN = 30
ARGUMENT_LEN = 1000
ARGUMENT_STATUS_LEN = 30
REVIEW_LEN = 1000

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=FIRST_NAME_LEN)
    last_name = models.CharField(max_length=LAST_NAME_LEN)
    age = models.PositiveSmallIntegerField()
    balance = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=CATEGORY_NAME_LEN)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=TAG_LEN)

    def __str__(self):
        return self.name


class Offer(models.Model):
    description = models.CharField(max_length=OFFER_DESC_LEN)
    price = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    avaliability = models.CharField(max_length=200, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.category.name + " by " + self.user_profile.user.username


class MeetingStatus(models.Model):
    name = models.CharField(max_length=MEETING_STATUS_LEN)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    date = models.DateTimeField("data of the meeting")
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='teacher')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    agreed_price = models.PositiveSmallIntegerField()
    status = models.ForeignKey(MeetingStatus, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher.user.username + " teaches " + self.student.user.username + " " + self.offer.category.name


def cancelMeeting(meeting):
    meeting.student.balance += meeting.agreed_price
    meeting.student.save()
    meeting.delete()


def updateUserMeetings(currUser):
    meetings = Meeting.objects.filter(Q(student__user=currUser) | Q(teacher__user=currUser))
    took_place = MeetingStatus.objects.filter(name="took_place").first()
    now = timezone.now()
    for meeting in meetings:
        if meeting.date < now:
            if meeting.status.name == "pending":
                cancelMeeting(meeting)
            elif meeting.status.name == "agreed":
                meeting.status = took_place
                meeting.save()


class ArgumentStatus(models.Model):
    name = models.CharField(max_length=ARGUMENT_STATUS_LEN)

    def __str__(self):
        return self.name


class Argument(models.Model):
    victim = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='victim')
    accusesed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='accusesed')
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    message = models.CharField(max_length=ARGUMENT_LEN)
    status = models.ForeignKey(ArgumentStatus, on_delete=models.CASCADE)

    def __str__(self):
        return self.victim.user.username + " accuses " + self.accusesed.user.username


class Review(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    reviewed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviewed')
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    rating = models.PositiveSmallIntegerField(range(0, 5))
    description = models.CharField(max_length=REVIEW_LEN, null=True)

    def __str__(self):
        return self.author.user.username + " reviews " + self.reviewed.user.username + " " + self.category.name
