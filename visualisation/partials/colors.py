#!/usr/bin/env python

# This file defines the COLORS list that contains the colors to use
# to display each piece id

# RGB values
COLORS = [
    [56, 29, 42],
    [62, 105, 144],
    [170, 189, 140],
    [233, 227, 180],
    [243, 155, 109],
    [238, 232, 44],
    [239, 183, 244]
]
# Keep the RGB values between 0 and 1
COLORS[:] = [[ele / 255 for ele in sub] for sub in COLORS]
