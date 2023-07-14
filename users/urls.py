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

from django.urls import path

from .views import (
    SignUpView,
    UserGroupCreateView,
    UserGroupListView,
    UserGroupDetailView,
    UserGroupAddMembersDetailView,
)

from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('groups/create/', UserGroupCreateView.as_view(), name='create_group'),
    path('groups/<int:pk>/', UserGroupDetailView.as_view(), name='group_detail'),
    path('groups/<int:pk>/add_members/',
         UserGroupAddMembersDetailView.as_view(),
         name='group_add_members'
         ),
    path('groups/', UserGroupListView.as_view(), name='group_list'),
    path('groups/<int:pk>/add_members_to_group/',
         views.add_members_to_group,
         name='add_members_to_group'
         ),
    path('groups/<int:pk>/remove_member_from_group/<int:id>/',
         views.remove_member_from_group,
         name='remove_member_from_group'
         ),
    path('groups/<int:pk>/delete/', views.delete_group, name='group_delete'),
]
