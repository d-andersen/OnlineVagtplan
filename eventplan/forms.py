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

from django import forms

from .models import Event, Shift
from tempus_dominus.widgets import DateTimePicker


class EventForm(forms.ModelForm):
    """Defines the form for creating a new Event"""

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        """Sets the model that the form should use, as well as which fields
        should be present in the form.
        """

        model = Event
        fields = (
            'title',
            'description',
        )


class ShiftForm(forms.ModelForm):
    """Defines the form for creating a new Shift"""

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    # start and end uses the Tempus Dominus Bootstrap module.
    # Source: https://tempusdominus.github.io/bootstrap-4/
    start = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
                'format': 'YYYY-MM-DD HH:mm',
                'stepping': '5',
                'sideBySide': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        )
    )
    end = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
                'format': 'YYYY-MM-DD HH:mm',
                'stepping': '5',
                'sideBySide': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        )
    )

    class Meta:
        """Sets the model that the form should use, as well as which fields
        should be present in the form.
        """

        model = Shift
        fields = (
            'shift_type',
            'description',
            'start',
            'end',
        )

    def clean(self):
        """Checks if an attempt is made to create a Shift which has an end time
        before its start time.

        Returns:
            None

        Raises:
            ValidationError: If an attempt is made to create a Shift which has
                an end time before its start time.
        """

        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end and (end < start):
            msg = "Shift end cannot be before shift start!"

            self.add_error('start', msg)
            self.add_error('end', msg)

            raise forms.ValidationError(
                "Shift end cannot be before shift start!"
            )
