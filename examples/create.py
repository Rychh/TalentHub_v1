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


cat = []
for name in categories:
    cat.append(Category.objects.create(name=name))

n1 = timezone.now() - timedelta(minutes=random.randint(1, 3000))
n2 = timezone.now() - timedelta(minutes=random.randint(3000, 9000))

pc = Profile.objects.all().count()

for i in range(100):
    n1 = timezone.now() - timedelta(minutes=random.randint(1, 3000))
    n2 = timezone.now() - timedelta(minutes=random.randint(3000, 9000))

    o = Offer.objects.create(description=desc[i % len(desc)],
                             price=random.randint(50, 150),
                             category=cat[i % len(cat)],
                             user_profile=Profile.objects.all()[i % pc],
                             avaliability=[[n1, n2]])
    o.tag.add(tags[i * 13 % 100])
    o.tag.add(tags[i * 19 % 100])
    o.tag.add(tags[i * i % 100])

ms1 = MeetingStatus(name='pending')
ms1.save()

ms2 = MeetingStatus(name='agreed')
ms2.save()

ms3 = MeetingStatus(name='took_place')
ms3.save()
ms4 = MeetingStatus(name='reviewed')
ms4.save()

asn = ["pending", "in progress", "ended"]
astab = []
for name in asn:
    a = ArgumentStatus(name=name)
    a.save()
    astab.append(a)

argument_message = ["She stole my money.",
    "I waited for him almost 2 hours!!!",
    "He knew nothing.", "Ligma"]

review_message = ["Nice.", "THX Dude",
    "He is a hero for me", 
    "To kondominium niemiecko-rosyjskie pod żydowskim zarządem powierniczym.",
    "djsnkasndksna", "Rychh is better.", "Poorly"]


for p in Profile.objects.all():
    cat = Category.objects.filter()
    for i in range(0,7):
        other_profiles = Profile.objects.exclude(user=p.user)
        opc = other_profiles.count()
        op = other_profiles[random.randint(0, opc - 1)]
        catc = cat.count()
        c = cat[random.randint(0, catc - 1)]
        rev = Review(author=p, reviewed=op, category=c, rating=i%6,
                description=review_message[i%7])
        rev.save()
            

for p in Profile.objects.all():
    ofers = Offer.objects.filter(user_profile=p)
    mss = MeetingStatus.objects.all()
    mss_argument = MeetingStatus.objects.filter(name="reviewed")[0]
    for i in range(min(15, ofers.count())):
        other_profiles = Profile.objects.exclude(user=p.user)
        opc = other_profiles.count()
        op = other_profiles[random.randint(0, opc - 1)]
       
        if i < 7: #<3
            m = Meeting(date=n1, agreed_price=10,
                    status=mss_argument, student=op,
                    teacher=p, offer=ofers[i])
            m.save()
            arg = Argument(victim=op, accusesed=p,
                        meeting=m, status=astab[i % len(astab)],
                        message=argument_message[i % len(argument_message)])
            arg.save()
        else:
            m = Meeting(date=n1, agreed_price=10,
                    status=mss[i % mss.count()], student=op,
                    teacher=p, offer=ofers[i])
            m.save()