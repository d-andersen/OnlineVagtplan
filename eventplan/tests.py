# 
# DM571 - Software Engineering - Fall Semester 2019
# 
# University of Southern Denmark
# 
# Project Part 2
# 
# LocalCinema Case Study - OnlineVagtplan System Implementation
# 
# 
# Authors:
# Dennis Andersen -- deand17
# Michael Hangaard Hansen -- michh16
# Mads Harloff Lauritsen -- madla17
# Eivind Roslyng-Jensen -- eiros15

from .models import *
from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class viewTests(TestCase):

    def test_login_status(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_home_redirect_to_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_login_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_userlist_view_and_template(self):
        response = self.client.get(reverse('event_news'))
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)


class ModelTests(TestCase):

    def test_shift_model_types(self):
        shiftTypes = ['TS','CS','MO','CL','FS','PR']
        counter = 0
        for shiftType in shiftTypes:
            testShift = Shift(shift_type=shiftType)
            testShift.save()
            if (testShift):
                counter = counter + 1
        self.assertEqual(counter, len(shiftTypes))

    def test_shift_model_unknown_types(self):
        shiftTypes = ['AA','RND']
        count = 0
        for shiftType in shiftTypes:
            try:
                testShift = Shift(shift_type=shiftType)
                testShift.save()
                if (testShift):
                    self.assertEqual(False)
            except:
                count = count + 1
        self.assertEqual(count, len(shiftTypes))

    def test_event_model(self):
        testEvent = Event(title='test Event', description="A test event")
        testEvent.save()
        if (testEvent):
            self.assertEqual(testEvent.title, 'test Event')
        else: self.assertTrue(False)

    def test_event_model_shift_count(self):
        testEvent = Event(title='test Event', description="A test event", id=1)
        self.assertEqual(testEvent.get_total_shift_count, 0)

    def test_event_model(self):
        testShifts = [Shift(shift_type='CL')]
        testEvent = Event(title='test Event', description="A test event")
        testShifts[0].save()
        testEvent.save()
        testEvent.shifts.set(testShifts)
        if (testEvent):
            self.assertEqual(testShifts[0].shift_type, 'CL')
        else: self.assertTrue(False)
