from django.db import models
from django.contrib.auth.models import User

FIRST_NAME_LEN = 20
LAST_NAME_LEN = 20
CATEGORY_NAME_LEN = 30
OFFER_DESC_LEN = 1000
TAG_LEN = 1000
MEETING_STATUS_LEN = 30


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=FIRST_NAME_LEN)
    last_name = models.CharField(max_length=LAST_NAME_LEN)
    age = models.PositiveSmallIntegerField()
    balance = models.PositiveIntegerField()

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


class Meeting(models.Model):
    date = models.DateTimeField("data of the meeting")
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='teacher')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    agreed_price = models.PositiveSmallIntegerField()
    status = models.ForeignKey(MeetingStatus, on_delete=models.CASCADE)
