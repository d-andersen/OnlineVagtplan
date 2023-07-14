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

from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#################### API testing ####################
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import EventSerializer
#####################################################

from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from .models import Event, Shift
from .forms import EventForm, ShiftForm

from onlinevagtplan.settings import TIME_ZONE
from onlinevagtplan.policies import SHIFT_CANCEL_DEADLINE


class EventListView(LoginRequiredMixin, ListView):
    """Class-based view for listing Events in the system.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        template_name: The name of the template used by this view.
        context_object_name: Specifies a custom name to be used by
            django's templating engine in place of 'object_list'.
        ordering: Specifies how model items should be ordered in
            the view. 'pk' orders items by primary key.
    """

    model = Event
    template_name = 'home.html'
    context_object_name = 'events'
    ordering = ['start']

    def get_context_data(self, **kwargs):
        """Context data is a dictionary that can be accessed by the django
        templating engine.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context dictionary updated with view-specific objects.
        """

        context = super().get_context_data(**kwargs)

        date = get_date(self.request.GET.get('date'))
        monday = date - timedelta(days=date.weekday())

        context['today'] = timezone.now()
        context['week'] = date

        # days is a list with the dates of the requested week that
        # we iterate over in the template to generate the calendar
        context['days'] = [0] * 7
        context['days'][0] = monday
        for i in range(1, 7):
            context['days'][i] = context['days'][0] + timedelta(days=i)

        # prev_week and next_week are strings we pass as GET requests
        # to calculate the dates for the previous and next week
        context['prev_week'] = make_date_str(monday - timedelta(days=7))
        context['next_week'] = make_date_str(monday + timedelta(days=7))

        return context


def get_date(datetime_str):
    """Convert a string representing a date in the format YYYY-MM-DD to an
    aware datetime object.
    
    Arguments:
        datetime_str: the date to be converted as a string. If the argument
            is None, the current date will be returned using django's
            timezone.now(), which is a timezone aware datetime object.
    
    Returns:
        datetime: The date as a datetime object.
    """

    if datetime_str:
        naive = datetime.strptime(datetime_str, '%Y-%m-%d')
        return pytz.timezone(TIME_ZONE).localize(naive, is_dst=None)

    return timezone.now()


def make_date_str(datetime_obj):
    """Convert a datetime object to a string of the format YYYY-MM-DD.
    
    Arguments:
        datetime_obj: the datetime object to be converted.
    
    Returns:
        str: The datetime object converted to a YYYY-MM-DD formatted string.
    """

    return 'date=' + datetime_obj.strftime('%Y-%m-%d')


class EventCreateView(LoginRequiredMixin, CreateView):
    """Class-based view for creating Events in the system.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        form_class: The form used by this view.
        template_name: The name of the template used by this view.
    """

    model = Event
    form_class = EventForm
    template_name = 'event_new.html'

    def form_valid(self, form):
        event = form.save(commit=False)
        event.created_by = self.request.user
        event.date_created = timezone.now()
        event.save()

        return redirect('event_manage', event.pk)


class EventDetailView(LoginRequiredMixin, DetailView):
    """Class-based view showing the details of an Event.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        template_name: The name of the template used by this view.
    """

    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        """Context data is a dictionary that can be accessed by the django
        templating engine.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context dictionary updated with view-specific objects.
        """

        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context


class ManageEventCreateView(LoginRequiredMixin, CreateView):
    """Class-based view for managing Events in the system.

    A user must be logged in to access this view.

    This is a multi-purpose view that provides the functionality for a
    specific Event to be edited or deleted, as well as allowing for
    Shifts to be added, edited, or removed from the Event.

    Apart from adding shifts to the Event, which is handled by this view,
    each of these actions are handled by different function-based views
    contained in this file. These are:

    Editing an event: is handled by the update_event() view.
    Deleting an event: is handled by the delete_event() view.
    Editing a shift: is handled by the update_shift() view.
    Deleting a shift: is handled by the delete_shift() view.

    Attributes:
        model: The model used by this view.
        form_class: The form used by this view.
        template_name: The name of the template used by this view.
    """

    model = Shift
    form_class = ShiftForm
    template_name = 'event_manage.html'

    def get_context_data(self, **kwargs):
        """Context data is a dictionary that can be accessed by the django
        templating engine.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context dictionary updated with view-specific objects.
        """

        context = super().get_context_data(**kwargs)

        event = Event.objects.get(pk=self.kwargs['pk'])
        shifts = event.shifts.all()
        update_event_form = EventForm
        update_shift_form = ShiftForm
        context['event'] = event
        context['shifts'] = shifts
        context['update_event_form'] = update_event_form
        context['update_shift_form'] = update_shift_form

        return context

    def form_valid(self, form):
        event = Event.objects.get(pk=self.kwargs['pk'])

        new_shift = create_new_shift(form)
        new_shift.save()
        event.shifts.add(new_shift)
        event.save()

        event.start = event.get_earliest_start
        event.end = event.get_latest_end
        event.save()

        return redirect('event_manage', event.pk)


def create_new_shift(form):
    """Creates a new Shift instance from the provided form data.

    Args:
        form: A form with the data needed to create a new Shift instance.

    Returns:
        Shift: A Shift based on the provided form data.
    """

    return Shift(
        shift_type=form.cleaned_data['shift_type'],
        description=form.cleaned_data['description'],
        start=form.cleaned_data['start'],
        end=form.cleaned_data['end'],
    )


@login_required
def update_event(request, **kwargs):
    """View for handling the request to update an Event.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect back to the 'event' page that sent the request.
    """

    event = Event.objects.get(pk=kwargs['pk'])

    if request.method == 'POST':

        form = EventForm(request.POST)
        if form.is_valid():
            event.title = form.cleaned_data['title']
            event.description = form.cleaned_data['description']
            event.save()

            messages.success(request,
                             f'Successfully updated the event!'
                             )
        else:
            messages.error(request,
                           f'Failed to update the event. The form you submitted \
                contained invalid data!'
                           )

    return redirect('event_manage', event.pk)


@login_required
def delete_event(request, **kwargs):
    """View for handling the request to delete an Event.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect back to the 'home' page.
    """

    if request.method == 'POST':
        event = Event.objects.get(pk=kwargs['pk'])
        for shift in event.shifts.all():
            shift.delete()

        event.delete()

        set_delete_event_success_message(request, event)

    return redirect('home')


def set_delete_event_success_message(request, event):
    return messages.success(request,
                            f'Successfully deleted the event {event.title}!'
                            )


@login_required
def update_shift(request, **kwargs):
    """View for handling the request to update a Shift.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect back to the 'manage event' page that sent the
            request.
    """

    event = Event.objects.get(pk=kwargs['pk'])
    shift = Shift.objects.get(pk=kwargs['id'])

    if request.method == 'POST':

        data = get_shift_data_from_post_request(request, shift.id)
        form = ShiftForm(data)

        if form.is_valid():
            shift.shift_type = form.cleaned_data['shift_type']
            shift.description = form.cleaned_data['description']
            shift.start = form.cleaned_data['start']
            shift.end = form.cleaned_data['end']
            shift.save()

            messages.success(request,
                             f'Successfully updated the shift!'
                             )
        else:
            messages.error(request,
                           f'Failed to update the event. The form you submitted \
                contained invalid data!'
                           )

    return redirect('event_manage', event.pk)


def get_shift_data_from_post_request(request, shift_id):
    """Place data from a POST request into a dictionary for form validation.

    Args:
        request: The sender request object.
        shift_id: The primary key of the Shift object the request is about.

    Returns:
        dict: A dictionary matching the form fields of a Shift.
    """
    return {
        'shift_type': request.POST[f'shift_type{shift_id}'],
        'description': request.POST['description'],
        'start': request.POST['start'],
        'end': request.POST['end']
    }


@login_required
def delete_shift(request, **kwargs):
    """View for handling the request to delete a Shift.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect back to the 'manage event' page that sent the
            request.
    """

    event = Event.objects.get(pk=kwargs['pk'])
    shift = Shift.objects.get(pk=kwargs['id'])

    if request.method == 'POST':
        shift.delete()

        messages.success(request,
                         f'Successfully deleted the shift!'
                         )

    return redirect('event_manage', event.pk)


@login_required
def take_shift(request, **kwargs):
    """View for handling the request from a user to take a Shift.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect back to the 'home' page.
    """

    shift = Shift.objects.get(pk=kwargs['id'])
    user = request.user
    date = timezone.localtime(shift.start)

    if shifts_overlap(user, shift):
        set_take_shift_overlap_error_message(request, shift)
        return redirect('/?date=' + date.strftime("%Y-%m-%d"))

    if request.method == 'POST':
        if not shift.volunteer:
            shift.volunteer = user
            shift.save()
            set_take_shift_success_message(request, shift)
        else:
            set_take_shift_error_message(request, shift)

    return redirect('/?date=' + date.strftime("%Y-%m-%d"))


def shifts_overlap(user, shift):
    """Check if a user has shifts already that overlap with the shift passed
    as the argument.

    Args:
        user: The user whose shifts should be checked.
        shift: The shift to be checked against for overlap.

    Returns:
        bool: Returns True if the user already has shifts that overlap with
            the passed shift argument, and False otherwise.
    """

    if user.shift_set.filter(end__gt=shift.start, start__lt=shift.end).exists():
        return True

    return False


def set_take_shift_success_message(request, shift):
    return messages.success(request,
                            f'Successfully signed you up for the shift \
                            "{shift.get_shift_type_display()}" on \
                            {shift.start.strftime("%m/%d/%Y, %H:%M")}!'
                            )


def set_take_shift_overlap_error_message(request, shift):
    return messages.error(request,
                          f'Could not sign you up for the shift \
                          "{shift.get_shift_type_display()}" on \
                          {shift.start.strftime("%m/%d/%Y, %H:%M")}, \
                          because it would overlap with another shift \
                          you have!'
                          )


def set_take_shift_error_message(request, shift):
    return messages.error(request,
                          f'Could not sign you up for the shift \
                "{shift.get_shift_type_display()}" on \
                {shift.start.strftime("%m/%d/%Y, %H:%M")}. \
                Shift is already taken!'
                          )


@login_required
def cancel_shift(request, **kwargs):
    """View for handling the request from a user to cancel a Shift.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect back to the 'home' page.
    """

    event = Event.objects.get(pk=kwargs['pk'])
    shift = Shift.objects.get(pk=kwargs['id'])
    user = request.user
    date = timezone.localtime(event.start)

    # Policy check. See policies.py
    if timezone.now() > (shift.start - timedelta(days=SHIFT_CANCEL_DEADLINE)):
        set_cancel_shift_past_deadline_error_message(request)
        return redirect('/?date=' + date.strftime("%Y-%m-%d"))

    if request.method == 'POST':
        if user == shift.volunteer:
            shift.volunteer = None
            shift.save()
            set_cancel_shift_success_message(request, shift)
        else:
            set_cancel_shift_error_message(request, shift)

    return redirect('/?date=' + date.strftime("%Y-%m-%d"))


def set_cancel_shift_past_deadline_error_message(request):
    return messages.error(request,
                          f'You cannot cancel shifts less than \
                          24 hours before they start!'
                          )


def set_cancel_shift_error_message(request, shift):
    return messages.error(request,
                          f'Could not cancel the shift \
                          "{shift.get_shift_type_display()}" on \
                          {shift.start.strftime("%m/%d/%Y, %H:%M")}. \
                          It is not your shift!'
                          )


def set_cancel_shift_success_message(request, shift):
    return messages.success(request,
                            f'Successfully canceled your sign up for the shift \
                            "{shift.get_shift_type_display()}" on \
                            {shift.start.strftime("%m/%d/%Y, %H:%M")}!'
                            )


""" ===============================================================
    API (Work In Progress)
    =============================================================== """


class APIEventListView(APIView):
    """
        TODO
    """

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# noinspection PyUnresolvedReferences
class APIEventDetailView(APIView):
    """
        TODO
    """

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Reponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
