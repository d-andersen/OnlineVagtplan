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
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    EventListView, 
    EventCreateView, 
    EventDetailView, 
    ManageEventCreateView,
)

from . import views

urlpatterns = [
    path('event/new/', EventCreateView.as_view(), name='event_new'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/manage/', ManageEventCreateView.as_view(), name='event_manage'),
    path('event/<int:pk>/update/', views.update_event, name='event_update'),
    path('event/<int:pk>/delete/', views.delete_event, name='event_delete'),
    path('event/<int:pk>/shift_update/<int:id>/', views.update_shift, name='shift_update'),
    path('event/<int:pk>/shift_delete/<int:id>/', views.delete_shift, name='shift_delete'),
    path('event/<int:pk>/shift_take/<int:id>/', views.take_shift, name='shift_take'),
    path('event/<int:pk>/shift_cancel/<int:id>/', views.cancel_shift, name='shift_cancel'),
    path('', EventListView.as_view(), name='home'),
    path('api/event_list/', views.APIEventListView.as_view(), name='api_event_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
