#!/usr/bin/env python

# Defines the COLORS list that contains the colors to use
# to display each piece id
# RGB values
COLORS = [
    [35, 61, 77],
    [254, 127, 45],
    [252, 202, 70],
    [161, 193, 129],
    [204, 51, 99],
    [40, 175, 176],
    [221, 206, 205]
]
# Keep the RGB values between 0 and 1
COLORS[:] = [[ele / 255 for ele in sub] for sub in COLORS]
