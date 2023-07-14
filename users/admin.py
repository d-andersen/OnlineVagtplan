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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserGroup


class CustomUserAdmin(UserAdmin):
    """Defines how a CustomUser should look in django's admin system."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'last_login',
        'date_joined',
    ]


# Register CustomUser, CustomUserAdmin and UserGroup in django admin.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserGroup)
