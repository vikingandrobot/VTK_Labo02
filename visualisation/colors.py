# Defines the COLORS list that contains the color to use
# to display each piece id

COLORS = [
    [35, 61, 77],
    [254, 127, 45],
    [252, 202, 70],
    [161, 193, 129],
    [97, 155, 138],
    [40, 175, 176],
    [221, 206, 205]
]
# Keep the RGB values between 0 and 1
COLORS[:] = [[ele / 255 for ele in sub] for sub in COLORS]
