import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import time

# ---------------------------
# Cube vertices and colors
# ---------------------------
vertices = [
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1],
]

colors = [
    [1, 0, 0],  # red
    [0, 1, 0],  # green
    [0, 0, 1],  # blue
    [1, 1, 0],  # yellow
    [1, 0, 1],  # magenta
    [0, 1, 1],  # cyan
]

# Each face is a list of 4 vertex indices
faces = [
    [0, 1, 2, 3],  # back
    [4, 5, 6, 7],  # front
    [0, 4, 7, 3],  # left
    [1, 5, 6, 2],  # right
    [3, 2, 6, 7],  # top
    [0, 1, 5, 4],  # bottom
]

def draw_cube():
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i % len(colors)])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

# ---------------------------
# Main rendering function
# ---------------------------
def main():
    # Initialize GLFW
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "OpenGL Rotating Cube (GLFW)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    # Setup perspective projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    last_time = time.time()
    angle = 0.0

    while not glfw.window_should_close(window):
        # Time-based rotation (smooth independent of frame rate)
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        angle += 50.0 * delta_time  # degrees per second

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Move camera back and rotate cube
        glTranslatef(0.0, 0.0, -6.0)
        glRotatef(angle, 1.0, 1.0, 0.0)

        draw_cube()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
