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

"""
    This file defines policy settings for the OnlineVagtplan system.
"""

"""
    Defines the deadline in days for when a shift can be canceled.
    For example, if a shift starts November 19, 2019 at 18:00, a
    policy of 1 day defines that a signup for a shift can be canceled
    up until, but not past, November 18, 2019 at 18:00.
"""
SHIFT_CANCEL_DEADLINE = 1
