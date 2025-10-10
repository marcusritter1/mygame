import glfw
from OpenGL.GL import *
from math import cos, sin, radians

tile_width = 64
tile_height = 32

def draw_tile(x, y, color):
    # Convert grid to isometric screen coordinates
    sx = (x - y) * (tile_width / 2)
    sy = (x + y) * (tile_height / 2)

    # Define diamond vertices (centered on sx, sy)
    vertices = [
        (sx, sy - tile_height / 2),   # top
        (sx + tile_width / 2, sy),    # right
        (sx, sy + tile_height / 2),   # bottom
        (sx - tile_width / 2, sy),    # left
    ]

    glColor3fv(color)
    glBegin(GL_QUADS)
    for vx, vy in vertices:
        glVertex2f(vx, vy)
    glEnd()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Isometric Tiles", None, None)
    glfw.make_context_current(window)

    glClearColor(0.2, 0.3, 0.4, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Set orthographic projection (2D)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, 300, -300, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Draw a small grid of tiles
        for y in range(5):
            for x in range(5):
                color = (0.3 + 0.1 * x, 0.5 + 0.05 * y, 0.3, )
                draw_tile(x, y, color)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
