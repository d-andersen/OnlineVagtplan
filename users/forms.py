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

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Defines the form for creating a new CustomUser"""

    class Meta(UserCreationForm.Meta):
        """Sets the model that the form should use, as well as which fields
        should be present in the form.
        """

        model = CustomUser
        fields = (
            'username', 
            'password1',
            'password2',
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
        )


class CustomUserChangeForm(UserChangeForm):
    """Defines the form for editing a CustomUser"""

    class Meta:
        """Sets the model that the form should use, as well as which fields
        should be present in the form.
        """

        model = CustomUser
        fields = UserChangeForm.Meta.fields
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
        )


