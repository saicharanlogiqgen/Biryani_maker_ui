"""GPIO pin configuration for the Biryani Maker (BCM numbering)."""

# Mixer motor
M1_PIN = 5

# Position motor
M2_F = 6
M2_B = 13

# Rice bowl hydraulic
V1_F = 17
V1_B = 27

# Mixer hydraulic
V2_F = 22
V2_B = 23

# Electronic valve
EV_OPEN = 24
EV_CLOSE = 25

ACTIVE_LOW = True

ALL_PINS = [
    M1_PIN,
    M2_F,
    M2_B,
    V1_F,
    V1_B,
    V2_F,
    V2_B,
    EV_OPEN,
    EV_CLOSE,
]
