from math import sin, cos

import numpy as np


def from_size_and_angle(magnitude: float, angle: float):
    return np.array([cos(angle), sin(angle)]) * magnitude


def norm(v: np.array) -> float:
    return np.linalg.norm(v, ord=1)


def normalize(v: np.array) -> np.array:
    length = norm(v)
    if length == 0:
        length = np.finfo(v.dtype).eps
    return v / length


def resize(v: np.array, magnitude) -> np.array:
    return normalize(v) * magnitude


def rotate(v: np.array, angle: float, axis: np.array) -> np.array:
    s = sin(angle)
    c = cos(angle)
    k = 1.0 - c
    x = v[0]
    y = v[1]
    z = v[2]
    axis_x = axis[0]
    axis_y = axis[1]
    axis_z = axis[2]

    nx = (
            x * (c + k * axis_x * axis_x) +
            y * (k * axis_x * axis_y - s * axis_z) +
            z * (k * axis_x * axis_z + s * axis_y)
    )

    ny = (
            x * (k * axis_x * axis_y + s * axis_z) +
            y * (c + k * axis_y * axis_y) +
            z * (k * axis_y * axis_z - s * axis_x)
    )

    nz = (
            x * (k * axis_x * axis_z - s * axis_y) +
            y * (k * axis_y * axis_z + s * axis_x) +
            z * (c + k * axis_z * axis_z)
    )

    return np.array([nx, ny, nz])
