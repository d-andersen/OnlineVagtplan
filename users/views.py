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

from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import CustomUserCreationForm
from .models import CustomUser, UserGroup

from eventplan.models import Shift


class SignUpView(CreateView):
    """Class-based view responsible for showing the signup form.

    Upon registering, a new CustomUser is created and the new user is
    redirected to the login page.

    Attributes:
        form_class: The form used by this view.
        success_url: The url which should be followed on successful
            form submission.
        template_name: The name of the template used by this view.
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserListView(LoginRequiredMixin, ListView):
    """Class-based view listing the users in the system.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        template_name: The name of the template used by this view.
        context_object_name: Specifies a custom name to be used by
            django's templating engine in place of 'object_list'.
    """

    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserGroupCreateView(LoginRequiredMixin, CreateView):
    """Class-based view for creating a new UserGroup.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        template_name: The name of the template used by this view.
        fields: The fields that should show up in the form rendered
            by this view.
    """

    model = UserGroup
    template_name = 'group_new.html'
    fields = ('title', 'group_type', 'description',)


class UserGroupListView(LoginRequiredMixin, ListView):
    """Class-based view for listing UserGroups in the system.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        template_name: The name of the template used by this view.
        context_object_name: Specifies a custom name to be used by
            django's templating engine in place of 'object_list'.
        ordering: Specifies how model items should be ordered in
            the view. 'pk' orders items by primary key.
    """

    model = UserGroup
    template_name = 'group_list.html'
    context_object_name = 'groups'
    ordering = ['pk']

    def get_context_data(self, **kwargs):
        """Context data is a dictionary that can be accessed by the django
        templating engine.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context dictionary updated with view-specific objects.
        """

        context = super().get_context_data(**kwargs)

        users = CustomUser.objects.all()
        context['users'] = users

        return context


class UserGroupDetailView(LoginRequiredMixin, DetailView):
    """Class-based view showing the details of a UserGroup.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        template_name: The name of the template used by this view.
        context_object_name: Specifies a custom name to be used by
            django's templating engine in place of 'object_list'.
    """

    model = UserGroup
    template_name = 'group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        """Context data is a dictionary that can be accessed by the django
        templating engine.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context dictionary updated with view-specific objects.
        """

        context = super().get_context_data(**kwargs)

        this_group_type = UserGroup.objects.get(pk=self.kwargs['pk']).group_type
        shifts = Shift.objects.filter(shift_type=this_group_type)
        context['today'] = timezone.now()
        context['shifts'] = shifts

        return context


class UserGroupAddMembersDetailView(LoginRequiredMixin, DetailView):
    """Class-based view showing the details of a UserGroup.

    A user must be logged in to access this view.

    Attributes:
        model: The model used by this view.
        template_name: The name of the template used by this view.
        context_object_name: Specifies a custom name to be used by
            django's templating engine in place of 'object_list'.
    """

    model = UserGroup
    template_name = 'group_add_users.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        """Context data is a dictionary that can be accessed by the django
        templating engine.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context dictionary updated with view-specific objects.
        """

        context = super().get_context_data(**kwargs)

        users = CustomUser.objects.all()
        context['users'] = users

        return context


@login_required
def add_members_to_group(request, **kwargs):
    """View for handling the request for adding members to a UserGroup.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect to the 'add members to group' page.
    """

    group = UserGroup.objects.get(pk=kwargs['pk'])

    if request.method == 'POST':
        selected_values = request.POST.getlist('selected_user')

        members_in_group = group.members.all()
        queryset = CustomUser.objects.filter(
            pk__in=list(map(int, selected_values))
        )

        for user in queryset:
            if user not in members_in_group:
                group.members.add(user)
                group.save()

        set_add_members_to_group_success_message(request, group)

    return redirect('group_add_members', group.pk)


def set_add_members_to_group_success_message(request, group):
    return messages.success(request,
                            f'Successfully added selected users as members to\
                            the {group.title} group!')


@login_required
def remove_member_from_group(request, **kwargs):
    """View for handling the request to remove a member from a UserGroup.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect to the page provided by the 'next'
            value in the sending form.
    """

    next_page = request.POST.get('next', '/')

    if request.method == 'POST':
        group = UserGroup.objects.get(pk=kwargs['pk'])
        members_in_group = group.members.all()
        user = CustomUser.objects.get(pk=kwargs['id'])

        if user in members_in_group:
            group.members.remove(user)
            group.save()

        set_remove_member_from_group_success_message(request, user, group)

    return HttpResponseRedirect(next_page)


def set_remove_member_from_group_success_message(request, user, group):
    return messages.success(request,
                            f'Successfully removed member {user.username} \
                            from the {group.title} group!'
                            )


@login_required
def delete_group(request, **kwargs):
    """View for handling the request to delete a UserGroup.

    A user must be logged in to access this view.

    Args:
        request: The sender request object.
        **kwargs: Additional keyword arguments.

    Returns:
        redirect: A redirect to the 'group list' page.
    """

    if request.method == 'POST':
        group = UserGroup.objects.get(pk=kwargs['pk'])
        group.delete()

        set_delete_group_success_message(request, group)

    return redirect('group_list')


def set_delete_group_success_message(request, group):
    return messages.success(request,
                            f'Successfully deleted the group {group.title}!'
                            )
