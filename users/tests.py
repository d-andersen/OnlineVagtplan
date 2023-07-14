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

class userModelstest(TestCase):

    def test_customUser_model(self):
        testUser = CustomUser(
            first_name = 'Test',
            last_name = 'User',
            email = 'example@example.com',
            phone_number = '12345678'
        )
        testUser.save()
        if (testUser):
            self.assertEqual(testUser.first_name, 'Test')
        else: self.assertTrue(False)

    
#Note that these entries are not actually accepted in the online textfield 
#even if the test asserts as false
    def test_customUser_model_email(self):
        testInput = [',',' ','1234','@none','@']
        boo = True
        for test in testInput:
            try:
                testUser = CustomUser(
                    username = test,
                    first_name = 'Test',
                    last_name = 'User',
                    email = test,
                    phone_number = '12345678'
                )
                testUser.save()
                if (testUser):
                    print()
                    print (test, "Was regarded as a valid email")
                    boo = False
            except: 
                print ("", end = '')
        self.assertTrue(boo)
    

    def test_customUser_model_phone(self):
        testInput = [',','','1234','@none','@']
        boo = True
        for test in testInput:
            try:
                testUser = CustomUser(
                    first_name = 'Test',
                    last_name = 'User',
                    email = 'example@example.com',
                    phone_number = test
                )
                testUser.save()
                if (testUser):
                    print()
                    print (test, "Was regarded as a valid phone number")
                    boo = False
            except: 
                print("", end = '')
        self.assertTrue(boo)


    def test_userGroup_model(self):
        groupTypes = ['TS','CS','MO','CL','FS','PR','OT']
        count = 0
        for groupType in groupTypes:
            testGroup = UserGroup(
                title = 'Test Group',
                group_type = groupType
            )
            testGroup.save()
            if (testGroup):
                count = count + 1
        self.assertEqual(count, len(groupTypes))

    def test_userGroup_model_unknown_types(self):
        groupTypes = ['AA', 'RND']
        count = 0
        for groupType in groupTypes:
            try:
                testGroup = UserGroup(
                    title = 'Test Group',
                    group_type = groupType
                )
                if (testGroup):
                    self.assertTrue(False)
            except:
                count = count + 1
        self.assertEqual(count, len(groupTypes))

    
    def test_userGroup_model_entry(self):
        testGroup = UserGroup(
            title = 'Test Group',
            group_type = 'OT',
        )

        testUser = CustomUser(
            first_name = 'Test',
            last_name = 'User',
            email = 'example@example.com',
            phone_number = '12345678',
        )
        testGroup.save()
        testUser.save()
        users = [testUser]
        testGroup.members.set(users)

        self.assertEqual(testGroup.num_members, 1)
    