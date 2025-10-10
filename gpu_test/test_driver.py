from OpenGL.GL import *
from OpenGL.GLUT import *

glutInit()
glutCreateWindow(b"GPU Check")
print("OpenGL Vendor:", glGetString(GL_VENDOR).decode())
print("Renderer:", glGetString(GL_RENDERER).decode())
print("Version:", glGetString(GL_VERSION).decode())
