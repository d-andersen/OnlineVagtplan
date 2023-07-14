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
# Source:
# https://www.django-rest-framework.org/tutorial/1-serialization/
# 

from rest_framework.serializers import ModelSerializer
from .models import Event


class EventSerializer(ModelSerializer):
    """Defines a serializer for the API framework"""

    class Meta:
        """Sets the model that the serializer should use, as well as which
        fields should be present.
        """
        model = Event
        fields = ['id', 'title', 'start', 'end', 'shifts']
