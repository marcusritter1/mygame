import pygame
from pause import PauseMenu
from quit_popup import QuitPopup
from map import Map
from util import split_evenly
import numpy as np

class Game:
    
    def __init__(self, screen, game_resolution):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Load textures
        self.water_texture = pygame.image.load("assets/water.png").convert_alpha()
        self.grass_texture = pygame.image.load("assets/grass.png").convert_alpha()
        
        self.map = Map()
        self.map_tiles_width = self.map.get_map_tiles_width()
        self.map_tiles_height = self.map.get_map_tiles_height()

        self.scroll_speed = 1
        self.margin = 0.1    # margin in % for scroll area to screen border

        self.camera_x = 0
        self.camera_y = 0

        self.game_screen_width = game_resolution[0]
        self.game_screen_height = game_resolution[1]

        
        """self.x_pos = 100  # Starting position of the animated object (circle)
        self.y_pos = 100
        self.x_velocity = 5  # Speed of the animation (movement per frame)
        self.y_velocity = 3  # Vertical speed of the animation"""
        
        self.tile_size = 50  # Each tile is 50x50 pixels
        
        self.grid_width = game_resolution[0] // self.tile_size
        if (game_resolution[0] / self.tile_size) > self.grid_width:
            self.grid_width += 1
        self.grid_height = game_resolution[1] // self.tile_size
        if (game_resolution[1] / self.tile_size) > self.grid_height:
            self.grid_height += 1

        if self.map_tiles_width < self.grid_width:
            missing_tiles_width = self.grid_width - self.map_tiles_width
            missing_tiles_left, missing_tiles_right = split_evenly(missing_tiles_width)
            self.map.tile_grid = np.pad(self.map.tile_grid, pad_width=((0, 0), (missing_tiles_left, missing_tiles_right)), mode='constant', constant_values=0)
            
        if self.map_tiles_height < self.grid_height:
            missing_tiles_height = self.grid_height - self.map_tiles_height
            missing_tiles_bottom, missing_tiles_top = split_evenly(missing_tiles_height)
            top_padding = np.zeros((missing_tiles_top, self.map.tile_grid.shape[1]), dtype=int)
            bottom_padding = np.zeros((missing_tiles_bottom, self.map.tile_grid.shape[1]), dtype=int)
            self.map.tile_grid = np.vstack((top_padding, self.map.tile_grid, bottom_padding))
        
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        self.tile_colors = {
            2: self.GREEN,  # Grass
            1: self.BLUE,   # Ocean
            0: self.BLACK   # Empty
        }

        self.tile_textures = {
            1: self.water_texture,  # ocean
            2: self.grass_texture  # grass
        }

        #print(self.grid_width * self.tile_size, self.game_screen_width)
        self.max_move_left_right = abs(self.game_screen_width - (self.grid_width * self.tile_size))
        self.max_move_up_down = abs(self.game_screen_height - (self.grid_height * self.tile_size))

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #print("mouse x:",mouse_x, "mouse y:",mouse_y)
            #print("camera_x:",self.camera_x, "camera_y:",self.camera_y)

            # scroll right
            if mouse_x >= self.game_screen_width - (self.game_screen_width * self.margin):
                if self.camera_x > -(self.max_move_left_right):
                    self.camera_x -= self.scroll_speed
            
            # scroll left
            if mouse_x <= self.game_screen_width * self.margin:
                if self.camera_x < 0:
                    self.camera_x += self.scroll_speed
            
            # scroll up
            if mouse_y <= self.game_screen_height * self.margin:
                if self.camera_y < 0:
                    self.camera_y += self.scroll_speed
            
            # scroll down
            if mouse_y >= self.game_screen_height - (self.game_screen_height * self.margin):
                if self.camera_y > -(self.max_move_up_down):
                    self.camera_y -= self.scroll_speed


            """# Create a simple animated object (moving circle)
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x_pos, self.y_pos), 20)

            # Update the position of the circle to create animation
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity

            # Bounce the circle off the walls
            if self.x_pos >= self.screen.get_width() - 20 or self.x_pos <= 20:
                self.x_velocity = -self.x_velocity  # Reverse horizontal direction
            if self.y_pos >= self.screen.get_height() - 20 or self.y_pos <= 20:
                self.y_velocity = -self.y_velocity  # Reverse vertical direction"""
                
            # Loop over the visible portion of the grid and draw tiles
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    tile_type = self.map.tile_grid[row][col]
                    if tile_type != 0:
                        self.screen.blit(self.tile_textures.get(tile_type, self.BLACK), (col * self.tile_size + self.camera_x, row * self.tile_size + self.camera_y))
                    else:
                        tile_rect = pygame.Rect(col * self.tile_size + self.camera_x, row * self.tile_size + self.camera_y, self.tile_size, self.tile_size)
                        pygame.draw.rect(self.screen, self.tile_colors.get(tile_type, self.BLACK), tile_rect)
                        pygame.draw.rect(self.screen, self.WHITE, tile_rect, 1)  # Grid outline

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = self.ask_quit()  # Show quit popup on window close
                    if result == "exit":
                        self.running = False
                        return "menu"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.toggle_pause()
                    elif event.key == pygame.K_ESCAPE:
                        result = self.ask_quit()  # Show quit popup on window close
                        if result == "exit":
                            self.running = False
                            return "menu"

            # Show the pause menu if the game is paused
            if self.paused:
                pause_menu = PauseMenu(self.screen)
                response = pause_menu.run()  # Pause menu blocks until resumed
                if response == "exit":
                    return "menu"
                else:
                    self.paused = False  # Unpause after returning from pause menu
            
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS

    def toggle_pause(self):
        """Toggles pause state."""
        self.paused = not self.paused

    def ask_quit(self):
        """Shows quit confirmation menu and processes response."""
        quit_popup = QuitPopup(self.screen)
        response = quit_popup.wait_for_response()
        if response == "Yes":
            return "exit"  # Signal to exit to the main menu
        elif response == "No":
            return None  # Stay in the game

