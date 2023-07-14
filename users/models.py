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
# 
# Last edit:
# November 21, 2019
# 

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.urls import reverse


class CustomUser(AbstractUser):
    """Defines a custom user model for the OnlineVagtplan system.

    Inherits from AbstractUser, meaning CustomUser has the same
    model fields as a User, so only required fields in addition to
    username and password are defined here.
    
    For the full list of fields of the User class see
    https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User

    Attributes:
        first_name: A model charfield specifying the first name of
            the user.
        last_name: A model charfield specifying the last name of
            the user.
        email: A model emailfield specifying the email of the user.
        phone_number: A model charfield specifying the phone number
            of the user.
    """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=30)


class UserGroup(models.Model):
    """Defines a custom user group model for the OnlineVagtplan system.

    A group has a title, a description and a number of members. The number
    of members can be zero.

    In addition, a group is associated with a type upon creation, which
    corresponds to the different shift types in the system (see the Shift
    class in eventplan.models), but without being directly connected. This
    makes the two models independent, but allows for showing shifts in a
    group that match a group's type.

    Attributes:
        title: A model charfield specifying the title of this UserGroup.
        group_type: A model choices field specifying the type of this
            UserGroup. Corresponds to the types of a Shift (see
            eventplan.Shift).
        members: A many to many relation to CustomUsers. That is, a
            CustomUser can be a member of many UserGroups and a UserGroup
            can have many different members.
        description: A model textfield specifying a description for this
            UserGroup.
    """

    TICKET_SELLING = 'TS'
    CANDY_SELLING = 'CS'
    MOVIE_OPERATION = 'MO'
    CLEANING = 'CL'
    FACILITY_SERVICE = 'FS'
    PR = 'PR'
    OT = 'OT'
    GROUP_TYPE_CHOICES = [
        (None, 'Choose group type'),
        (TICKET_SELLING, 'Ticket Selling'),
        (CANDY_SELLING, 'Candy Selling'),
        (MOVIE_OPERATION, 'Movie Operation'),
        (CLEANING, 'Cleaning'),
        (FACILITY_SERVICE, 'Facility Service'),
        (PR, 'PR Work'),
        (OT, 'Other'),
    ]
    title = models.CharField(max_length=200)
    group_type = models.CharField(
        max_length=2,
        choices=GROUP_TYPE_CHOICES,
    )
    members = models.ManyToManyField('users.CustomUser', blank=True)
    description = models.TextField(blank=True)

    @property
    def num_members(self):
        """Returns the number of members of this UserGroup.
        
        Returns:
            int: The number of members of this UserGroup.
        """
        
        count = self.members.all().aggregate(Count('pk'))
        return count['pk__count']

    def __str__(self):
        """Use the title of this UserGroup as its string representation.
        
        Returns:
            str: The title of this UserGroup as a string.
        """

        return self.title

    def get_absolute_url(self):
        """Returns the full path to the UserGroup as a string.

        The full path to a particular group is retrieved by passing the id of
        the current UserGroup instance, which is equivalent to passing the
        primary key.

        Returns:
            str: the full path to the group as a string.
        """

        return reverse('group_detail', args=[str(self.id)])
