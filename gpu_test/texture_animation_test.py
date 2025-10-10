import glfw
from OpenGL.GL import *
from PIL import Image
import time

# --- texture functions ---
def load_texture(path):
    img = Image.open(path).convert("RGBA")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)  # flip vertically
    img_data = img.tobytes()
    width, height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    return tex_id, width, height

def draw_tile_with_frame(x, y, tex_id, frame, total_frames, tile_width=32, tile_height=32):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glEnable(GL_TEXTURE_2D)

    u0 = frame / total_frames
    u1 = (frame + 1) / total_frames
    v0 = 0.0
    v1 = 1.0

    sx = (x - y) * (tile_width / 2)
    sy = (x + y) * (tile_height / 2)

    glBegin(GL_QUADS)
    glTexCoord2f(u0, v1); glVertex2f(sx - tile_width/2, sy - tile_height/2)
    glTexCoord2f(u1, v1); glVertex2f(sx + tile_width/2, sy - tile_height/2)
    glTexCoord2f(u1, v0); glVertex2f(sx + tile_width/2, sy + tile_height/2)
    glTexCoord2f(u0, v0); glVertex2f(sx - tile_width/2, sy + tile_height/2)
    glEnd()

    glDisable(GL_TEXTURE_2D)

# --- main ---
if not glfw.init():
    exit()

window = glfw.create_window(800, 600, "Isometric Tile Animation", None, None)
glfw.make_context_current(window)

# 2D orthographic projection
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-400, 400, 300, -300, -1, 1)
glMatrixMode(GL_MODELVIEW)

# Load sprite sheet
tex_id, tex_width, tex_height = load_texture("../assets/CatPackFree/CatPackFree/Idle.png")

# Animation variables
total_frames = 10
current_frame = 0
frame_duration = 0.1
last_time = time.time()

while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Update frame
    now = time.time()
    if now - last_time > frame_duration:
        current_frame = (current_frame + 1) % total_frames
        last_time = now

    # Draw animated tile
    draw_tile_with_frame(x=2, y=1, tex_id=tex_id, frame=current_frame, total_frames=total_frames)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
