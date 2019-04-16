import random
from talenthub.models import *
from datetime import timedelta
from django.utils import timezone
from .desc_list import *

categories = ["Maths",
              "Algebra",
              "Geometry",
              "Science",
              "Biology",
              "Physics",
              "Chemistry",
              "Geography",
              "History",
              "Citizenship",
              "Physical Education",
              "Business Studies",
              "Home Economics",
              "Cooking",
              "Art",
              "Music"]

tags = []
for i in range(100):
    t = Tag(name="tag" + str(i))
    t.save()
    tags.append(t)


if User.objects.count() < 2:
    u = User.objects.create(username='user123', password='password')
    u2 = User.objects.create(username='user234', password='password')
else:
    u = User.objects.all()[0]
    u2 = User.objects.all()[1]

if Profile.objects.count() < 2:
    p = Profile.objects.create(user=u, first_name='dumbest_name',
                               last_name='dumbest_last_name',
                               age=22, balance=14)
    p2 = Profile.objects.create(user=u2, first_name='dumb_name',
                                last_name='dumb_last_name',
                                age=54, balance=120)
else:
    p = Profile.objects.all()[0]
    p2 = Profile.objects.all()[1]

cat = []
for name in categories:
    cat.append(Category.objects.create(name=name))

n1 = timezone.now() - timedelta(minutes=random.randint(1, 3000))
n2 = timezone.now() - timedelta(minutes=random.randint(3000, 9000))

for i in range(100):
    n1 = timezone.now() - timedelta(minutes=random.randint(1, 3000))
    n2 = timezone.now() - timedelta(minutes=random.randint(3000, 9000))

    o = Offer.objects.create(description=desc[i % len(desc)],
                             price=random.randint(50, 150),
                             category=cat[i % len(cat)],
                             user_profile=p,
                             avaliability=[[n1, n2]])
    o.tag.add(tags[i * 13 % 100])
    o.tag.add(tags[i * 19 % 100])
    o.tag.add(tags[i * i % 100])

ms1 = MeetingStatus(name='pending')
ms1.save()

ms2 = MeetingStatus(name='agreed')
ms2.save()

for i in range(10):
    oc = Offer.objects.count()
    o1 = Offer.objects.all()[i % oc]
    o2 = Offer.objects.all()[(17 * i + 1) % oc]
    m1 = Meeting(date=n1, agreed_price=10,
                 status=ms1, student=p,
                 teacher=p2, offer=o1)
    m1.save()
    m2 = Meeting(date=n1, agreed_price=10,
                 status=ms2, student=p2,
                 teacher=p, offer=o2)
    m2.save()
