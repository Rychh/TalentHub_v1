from talenthub.models import (Category, User, Profile, Period,
                              Offer, MeetingStatus, Meeting)
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone


class DBTest(TestCase):

    def setUp(self):
        self.u = User(username='dummy', password='password')
        self.u.save()
        self.p = Profile(user=self.u, first_name='dumb_name',
                         last_name='dumb_last_name', age=22, balance=14)
        self.p.save()
        self.c = Category(name="Matma")
        self.c.save()

        self.o = Offer(description="this is a dumb offer",
                       tags=['tag1', 'tag2', 'tag3'],
                       price=100, category=self.c, user_profile=self.p)
        self.o.save()

        self.n1 = timezone.now()
        self.n2 = self.n1 - timedelta(days=1)

        self.per = Period(offer=self.o, date_from=self.n2, date_to=self.n1)
        self.per.save()

        self.ms = MeetingStatus(name='pending')
        self.ms.save()
        self.m = Meeting(date=self.n1, agreed_price=90, status=self.ms)
        self.m.save()

    def testPeriodSet(self):
        x = self.o.period_set.count()
        self.assertEqual(x, 1)

    def testTags(self):
        tags = self.o.tags
        self.assertEqual(len(tags), 3)
        self.assertTrue(tags[0] == 'tag1')

    def testCategories(self):
        self.assertTrue(self.o.category in
                        Category.objects.filter(name="Matma"))
