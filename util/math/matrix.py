import math

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

from util.math import vector


# gluPerspective(field_of_view, Global().aspect_ratio(), near, far)
def my_glu_perspective(fovy: float, aspect: float, z_near: float, z_far: float) -> None:
    fh = math.tan(fovy / 360.0 * math.pi) * z_near
    fw = fh * aspect
    glFrustum(-fw, fw, -fh, fh, z_near, z_far)


"""
void GLAPIENTRY
gluLookAt(GLdouble eyex, GLdouble eyey, GLdouble eyez, GLdouble centerx,
	  GLdouble centery, GLdouble centerz, GLdouble upx, GLdouble upy,
	  GLdouble upz)
{
    float forward[3], side[3], up[3];
    GLfloat m[4][4];

    forward[0] = centerx - eyex;
    forward[1] = centery - eyey;
    forward[2] = centerz - eyez;

    up[0] = upx;
    up[1] = upy;
    up[2] = upz;

    normalize(forward);

    /* Side = forward x up */
    cross(forward, up, side);
    normalize(side);

    /* Recompute up as: up = side x forward */
    cross(side, forward, up);

    __gluMakeIdentityf(&m[0][0]);
    m[0][0] = side[0];
    m[1][0] = side[1];
    m[2][0] = side[2];

    m[0][1] = up[0];
    m[1][1] = up[1];
    m[2][1] = up[2];

    m[0][2] = -forward[0];
    m[1][2] = -forward[1];
    m[2][2] = -forward[2];

    glMultMatrixf(&m[0][0]);
    glTranslated(-eyex, -eyey, -eyez);
}
"""


def my_glu_look_at(eye: np.array, target: np.array, up: np.array):
    gluLookAt(
        eye[0], eye[1], eye[2],
        target[0], target[1], target[2],
        up[0], up[1], up[2]
    )

    # side = vector.normalize(np.cross(target, up))
    # up = vector.normalize(np.cross(side, target))
    #
    # m = [
    #     [side[0], up[0], -target[0], 0],
    #     [side[1], up[1], -target[1], 0],
    #     [side[2], up[2], -target[2], 0],
    #     [0, 0, 0, 1]
    # ]
    #
    # glMultMatrixf(m)
    # glTranslatef(eye[0], eye[1], eye[2])
