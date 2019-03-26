from talenthub.models import *
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


        self.n1 = timezone.now()
        self.n2 = self.n1 - timedelta(days=1)

        self.o = Offer(description="this is a dumb offer",
                       price=100, category=self.c, user_profile=self.p,
                       avaliability=[[self.n1,self.n2]])
        self.o.save()

        self.tags = []
        for i in range(10):
            t = Tag(name="tag" + str(i))
            t.save()
            t.offer.add(self.o)
            self.tags.append(t)

        # self.per = Period(offer=self.o, date_from=self.n2, date_to=self.n1)
        # self.per.save()

        self.ms = MeetingStatus(name='pending')
        self.ms.save()
        self.m = Meeting(date=self.n1, agreed_price=90, status=self.ms)
        self.m.save()

    def testPeriod(self):
        # x = self.o.period_set.count()
        # self.assertEqual(x, 1)
        n1 = self.o.avaliability[0][0]
        n2 = self.o.avaliability[0][1]
        self.assertTrue(n1 - timedelta(days=1) == n2)
        self.assertTrue(self.n1 is n1)

    def testTags(self):
        tags = self.o.tag_set
        self.assertEqual(tags.count(), 10)
        t0 = tags.all().order_by('name')[0]
        self.assertTrue(t0.name == 'tag0')

    def testCategories(self):
        self.assertTrue(self.o.category in
                        Category.objects.filter(name="Matma"))
