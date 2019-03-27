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


if User.objects.count() == 0:
    u = User.objects.create(username='user123', password='password')
else:
    u = User.objects.all()[0]

if Profile.objects.count() == 0:
    p = Profile.objects.create(user=u, first_name='dumbest_name',
                               last_name='dumbest_last_name',
                               age=22, balance=14)
else:
    p = Profile.objects.all()[0]

cat = []
for name in categories:
    cat.append(Category.objects.create(name=name))

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
