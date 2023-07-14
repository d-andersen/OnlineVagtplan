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

from django.db import models
from django.db.models import Min, Max, Count
from django.utils import timezone
from django.urls import reverse

from datetime import timedelta

from users.models import CustomUser


class Shift(models.Model):
    """Defines a Shift model for the OnlineVagtplan system.

    A Shift has a type, a description, a start, and an end time, as well as
    a potential volunteer associated. The Shift type, start, and end times
    are required, but the description and volunteer fields can be blank.

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
    FACILITY_SERVICE ='FS'
    PR = 'PR'
    SHIFT_TYPE_CHOICES = [
        (None, 'Choose shift type'),
        (TICKET_SELLING, 'Ticket Selling'),
        (CANDY_SELLING, 'Candy Selling'),
        (MOVIE_OPERATION, 'Movie Operation'),
        (CLEANING, 'Cleaning'),
        (FACILITY_SERVICE, 'Facility Service'),
        (PR, 'PR Work'),
    ]
    shift_type = models.CharField(
        max_length=2,
        choices=SHIFT_TYPE_CHOICES,
    )
    description = models.TextField(blank=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    volunteer = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
    )

    class Meta:
        ordering = ['start']

    def __str__(self):
        """Use the type of this shift as its string representation.
        
        Returns:
            str: Return this shift represented as a string based on the type
                of the Shift.
        """

        return self.shift_type

    def get_absolute_url(self):
        """Returns the full path to this Shift as a string.
        
        Returns:
            str: The full path to this Shift as a string.
        """

        return reverse('shift_detail', args=[str(self.id)])


def event_end_offset():
    return timezone.now() + timedelta(hours=1)


class Event(models.Model):
    """Defines an Event model for the OnlineVagtplan system.

    An Event is intended as a container for shows and other events, which
    require a number of different Shifts.

    An Event has a title and a description, as well as a start and end time.
    An Event can also have a number of Shifts associated. In addition, an
    Event stores the user who created it, as well as when it was created.

    The created_by and date_created fields are currently not editable
    anywhere in the system. The same holds for the start and end fields,
    which are given default values when the Event is created, and then
    updated to match the start and end times of the Shifts associated with
    the Event. That is, the time frame of an Event is determined by the
    earliest start time and latest end time of all associated Shifts.

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

    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
    )
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=event_end_offset)
    shifts = models.ManyToManyField(Shift, related_name='events', blank=True)

    @property
    def get_earliest_start(self):
        """Returns the earliest start time of all associated Shifts.

        Returns:
            str: The earliest start time of all associated Shifts.
        """

        start = self.shifts.all().aggregate(Min('start'))
        return start['start__min']

    @property
    def get_latest_end(self):
        """Returns the latest end time of all associated Shifts.

        Returns:
            str: The latest end time of all associated Shifts.
        """

        end = self.shifts.all().aggregate(Max('end'))
        return end['end__max']

    @property
    def get_total_shift_count(self):
        """Returns the total number of Shifts associated with this Event.

        Returns:
            int: The total number of associated Shifts.
        """

        count = self.shifts.all().aggregate(Count('pk'))
        return count['pk__count']

    @property
    def get_free_shift_count(self):
        """Returns the number of Shifts associated with this Event that
        do not have a volunteer attached.

        Returns:
            int: The number of Shifts without a volunteer attached.
        """

        total = self.shifts.all().aggregate(Count('pk'))
        taken = self.shifts.all().aggregate(Count('volunteer'))
        not_taken = total['pk__count'] - taken['volunteer__count']
        started = self.shifts.filter(start__lte=timezone.now()).aggregate(Count('pk'))
        free = not_taken - started['pk__count']
        return max(0, free)

    def __str__(self):
        """Use the title of an Event as its string representation.
        
        Returns:
            str: Return the title of the Event as its string representation.
        """
        return self.title

    def get_absolute_url(self):
        """Returns the full path to the Event as a string.

        The full path to a particular Event is retrieved by passing the id of
        the current UserGroup instance, which is equivalent to passing the
        primary key.

        Returns:
            str: the full path to the group as a string.
        """

        return reverse('event_detail', args=[str(self.id)])
