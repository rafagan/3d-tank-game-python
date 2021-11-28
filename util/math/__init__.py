import math


def to_radians(angle_degree):
    return angle_degree * math.pi / 180.0


def to_degree(angle_radians):
    return angle_radians * 180.0 / math.pi
