import pygame
from pause import PauseMenu
from ingame_menu import InGameMenu
from map import Map
from util import split_evenly, cart_to_iso, screen_to_iso, calculate_map_padding
import numpy as np
from game_stats import GameStats
from game_settings import GameSettings


class Game:

    def __init__(self, screen, game_resolution, game_settings: GameSettings = None, new_game: bool = True, game_stats: GameStats = None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_settings = game_settings

        if new_game:
            self.game_stats = GameStats(gold=500)
        else:
            self.game_stats = game_stats

        self.last_update_time = pygame.time.get_ticks()  # Get initial time
        self.update_interval = 10000  # 10 seconds in milliseconds

        self.game_stats_bar_height = 30

        # Load textures
        self.water_texture = pygame.image.load("assets/tileset/tiles/tile_104.png").convert_alpha()
        self.grass_texture = pygame.image.load("assets/tileset/tiles/tile_022.png").convert_alpha()
        self.house_texture = pygame.image.load("assets/tileset/tiles/tile_044.png").convert_alpha()
        self.out_of_map_texture = pygame.image.load("assets/tileset/tiles/tile_092.png").convert_alpha()

        #DEBUG
        #print(self.water_texture.get_width(), self.water_texture.get_height())

        self.map = Map()
        self.map_tiles_width = self.map.get_map_tiles_width()
        self.map_tiles_height = self.map.get_map_tiles_height()

        print("map_tiles_width:", self.map_tiles_width)
        print("map_tiles_height:", self.map_tiles_height)

        self.scroll_speed = 4
        self.margin = 0.1    # margin in % for scroll area to screen border

        self.camera_x = 0
        self.camera_y = 0

        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.mouse_adjusted_x = 0.0
        self.mouse_adjusted_y = 0.0
        self.mouse_map_position_x = 0
        self.mouse_map_position_y = 0

        self.game_screen_width = game_resolution[0]
        self.game_screen_height = game_resolution[1]

        self.in_menu = False
        self.game_menue = InGameMenu(self.screen, self.game_screen_width, self.game_screen_height)

        self.object_selected = False
        self.selected_object_map_position_x = 0
        self.selected_object_map_position_y = 0

        """self.x_pos = 100  # Starting position of the animated object (circle)
        self.y_pos = 100
        self.x_velocity = 5  # Speed of the animation (movement per frame)
        self.y_velocity = 3  # Vertical speed of the animation"""

        self.texture_size = self.game_settings.texture_size[0]
        self.texture_width = self.game_settings.texture_size[0]
        self.texture_height = self.game_settings.texture_size[1]

        #TODO: DEBUG
        # Initialize camera position to center the map
        #self.camera_x = self.iso_map_width // 2 - self.game_screen_width // 2
        #self.camera_y = self.iso_map_height // 2 - self.game_screen_height // 2

        # calculate max tiles width and height that will fit on the game screen
        self.max_tiles_fit_screen_width = game_resolution[0] // self.texture_size
        if (game_resolution[0] / self.texture_size) > self.max_tiles_fit_screen_width:
            self.max_tiles_fit_screen_width += 1
        self.max_tiles_fit_screen_height = game_resolution[1] // self.texture_size
        if (game_resolution[1] / self.texture_size) > self.max_tiles_fit_screen_height:
            self.max_tiles_fit_screen_height += 1

        # if the map is smaller than the amount of tiles required to fill the game screen extend the map by padding it with empty tiles
        """if self.map_tiles_width < self.max_tiles_fit_screen_width:
            missing_tiles_width = self.max_tiles_fit_screen_width - self.map_tiles_width
            missing_tiles_left, missing_tiles_right = split_evenly(missing_tiles_width)
            self.map.tile_grid = np.pad(self.map.tile_grid, pad_width=((0, 0), (missing_tiles_left, missing_tiles_right)), mode='constant', constant_values=0)
            self.map_tiles_width = self.map.get_map_tiles_width()
        if self.map_tiles_height < self.max_tiles_fit_screen_height:
            missing_tiles_height = self.max_tiles_fit_screen_height - self.map_tiles_height
            missing_tiles_bottom, missing_tiles_top = split_evenly(missing_tiles_height)
            top_padding = np.zeros((missing_tiles_top, self.map.tile_grid.shape[1]), dtype=int)
            bottom_padding = np.zeros((missing_tiles_bottom, self.map.tile_grid.shape[1]), dtype=int)
            self.map.tile_grid = np.vstack((top_padding, self.map.tile_grid, bottom_padding))
            self.map_tiles_height = self.map.get_map_tiles_height()"""

        self.detail_view_width = 200
        self.detail_view_height = 100
        self.detail_view_text = ""

        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.LIGHT_GRAY = (200, 200, 200)

        self.font = pygame.font.Font(None, 24)

        self.tile_colors = {
            2: self.GREEN,  # Grass
            1: self.BLUE,   # Ocean
            0: self.BLACK   # Empty
        }

        self.tile_textures = {
            1: self.water_texture,  # ocean
            2: self.grass_texture,  # grass
            3: self.house_texture   # house
        }

        # Calculate the isometric map size
        self.iso_map_width = (self.map_tiles_width + self.map_tiles_height) * (self.texture_size // 2)
        self.iso_map_height = (self.map_tiles_width + self.map_tiles_height) * (self.texture_size // 4)

        #iso_origin_x = map_height * (tile_width // 2)
        #iso_origin_y = 0

        # calculate the max amount of pixels the camera can be moved on x and y axis depending on the map size
        if self.map_tiles_width < self.max_tiles_fit_screen_width:
            self.map_width_smaller_than_screen = True
            #self.max_move_left_right = abs(self.game_screen_width - (self.max_tiles_fit_screen_width * self.texture_size))
            self.max_move_left_right = self.iso_map_width - self.game_screen_width
        else:
            self.map_width_smaller_than_screen = False
            #self.max_move_left_right = abs(self.game_screen_width - (self.map_tiles_width * self.texture_size))
            self.max_move_left_right = self.iso_map_width - self.game_screen_width

        # check whether the map is smaller than the screen_width
        if self.map_tiles_height < self.max_tiles_fit_screen_height:
            self.map_height_smaller_than_screen = True
            print("MAP IS SMALLER THAN SCREEN!")
            #self.max_move_up_down = abs(self.game_screen_height - (self.max_tiles_fit_screen_height * self.texture_size / 2))
            self.max_move_up_down = -self.game_screen_height
        else:
            self.map_height_smaller_than_screen = False
            print("MAP IS BIGGER THAN SCREEN!")
            self.max_move_up_down = abs(self.game_screen_height - (self.map_tiles_height * self.texture_size / 2) - (self.texture_size // 8))

        """if self.map_width_smaller_than_screen is True:
            # Calculate max movement left and right
            self.max_move_left = 0  # The left edge of the map
            self.max_move_right = 0  # Right boundary
        else:
            # Calculate max movement left and right
            self.max_move_left = 0  # The left edge of the map
            self.max_move_right = self.iso_map_width - self.game_screen_width  # Right boundary

        if self.map_height_smaller_than_screen is True:
            # Calculate max movement up and down
            self.max_move_up = 0  # The top edge of the map
            self.max_move_down = -self.game_screen_height  # Bottom boundary
        else:
            # Calculate max movement up and down
            self.max_move_up = 0  # The top edge of the map
            self.max_move_down = self.iso_map_height - self.game_screen_height  # Bottom boundary"""

        # calculate the amount of padding needed so that there is no black screen shown in the game window
        self.map_padding = calculate_map_padding(self.game_screen_width, self.game_screen_height, self.texture_size)
        #self.map_padding = 10

        if self.map_tiles_height == self.map_tiles_width:
            offset_x = 0
            offset_y = 0
        else:
            offset_x = (self.map_tiles_width - self.map_tiles_height) / 2
            offset_y = 0.05 * self.map_tiles_width + 0.0556 * self.map_tiles_height - 0.1176
            offset_y = int(offset_y * 10) / 10.0
            #offset_y = 1.6


        print("DEBUG offset_x:", offset_x)
        print("DEBUG offset_y:", offset_y)

        # Calculate the starting position of the camera
        #self.camera_x = (self.game_screen_width // 2) - (self.iso_map_width // 2) #- (self.map_tiles_height*8) #(2*self.texture_size)
        self.camera_x = (self.game_screen_width / 2) - (self.iso_map_width / 2) - (offset_x*self.texture_size // 2)
        print("DEBUG camera X:", self.camera_x)
        self.camera_y = (self.game_screen_height // 2) - (self.iso_map_height // 4) + (self.texture_size // 2) + (offset_y*self.texture_size)

    def run(self):
        while self.running:

            # win condition
            if self.game_stats.gold >= 1000:
                self.running = False
                return "game_won"

            # loose condition
            if self.game_stats.gold <= -300:
                self.running = False
                return "game_lost"

            if self.in_menu:

                response = self.game_menue.wait_for_response(self.game_stats)
                if response == "exit":
                    self.running = False
                    return "menu"
                elif response == "continue":
                    self.in_menu = False
                    return None

            self.screen.fill((0, 0, 0))

            # Get mouse position
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            #print("mouse x:",self.mouse_x, "mouse y:",self.mouse_y)
            #print("camera_x:",self.camera_x, "camera_y:",self.camera_y)

            # calculate the adjusted mouse position on the map, considers the camera offset
            self.mouse_adjusted_x = self.mouse_x - self.camera_x
            self.mouse_adjusted_y = self.mouse_y - self.camera_y
            #print("mouse_adjusted_x:",self.mouse_adjusted_x, "mouse_adjusted_y:", self.mouse_adjusted_y)

            # calculate the grid position on the map the mouse is currently pointing at
            #screen_to_iso(mouse_x, mouse_y, tile_size, screen_width, screen_height, camera_x, camera_y)
            self.mouse_map_position_x, self.mouse_map_position_y = screen_to_iso(self.mouse_adjusted_x, self.mouse_adjusted_y, self.texture_size, self.game_screen_width, self.game_screen_height, self.camera_x, self.camera_y)
            #self.mouse_map_position_x = self.mouse_adjusted_x // self.texture_size
            #self.mouse_map_position_y = self.mouse_adjusted_y // self.texture_size
            #print("mouse_map_position_x:", self.mouse_map_position_x, "mouse_map_position_y:", self.mouse_map_position_y)

            # scroll right
            if self.mouse_x >= self.game_screen_width - (self.game_screen_width * self.margin):
                if self.camera_x > -(self.max_move_left_right):
                    test_camera_x = self.camera_x - self.scroll_speed
                    if test_camera_x < -(self.max_move_left_right):
                        diff = abs(test_camera_x) - (self.max_move_left_right)
                        move = self.scroll_speed - diff
                        self.camera_x -= move
                    else:
                        self.camera_x -= self.scroll_speed

            # scroll left
            if self.mouse_x <= self.game_screen_width * self.margin:
                if self.camera_x < 0:
                    test_camera_x = self.camera_x + self.scroll_speed
                    if test_camera_x > 0:
                        diff = 0 - abs(test_camera_x)
                        move = self.scroll_speed + diff
                        self.camera_x += move
                    else:
                        self.camera_x += self.scroll_speed

            # scroll up
            if self.mouse_y <= self.game_screen_height * self.margin:
                if self.camera_y < 0:
                    # the adjustments seems not to be needed for this move
                    test_camera_y = self.camera_y + self.scroll_speed
                    if test_camera_y > 0:
                        diff = 0 - abs(test_camera_y)
                        move = self.scroll_speed + diff
                        self.camera_y += move
                    else:
                        self.camera_y += self.scroll_speed

            # scroll down
            if self.mouse_y >= self.game_screen_height - (self.game_screen_height * self.margin):
                if self.camera_y > -(self.max_move_up_down):
                    test_camera_y = self.camera_y - self.scroll_speed
                    if test_camera_y < -(self.max_move_up_down):
                        diff = abs(test_camera_y) - (self.max_move_up_down)
                        move = self.scroll_speed - diff
                        self.camera_y -= move
                    else:
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

            # Extended loop to go beyond map boundaries
            for row in range(-self.map_padding, self.map_tiles_height + self.map_padding):
                for col in range(-self.map_padding, self.map_tiles_width + self.map_padding):

                    # Is this tile inside the actual map?
                    inside_map = (0 <= row < self.map_tiles_height) and (0 <= col < self.map_tiles_width)

                    # Convert to isometric coordinates
                    iso_x, iso_y = cart_to_iso(
                        col, row,
                        self.texture_size,
                        self.game_screen_width,
                        self.game_screen_height,
                        self.camera_x,
                        self.camera_y,
                        self.iso_map_width,
                        self.iso_map_height,
                        self.map_width_smaller_than_screen,
                        self.map_height_smaller_than_screen
                    )

                    if inside_map:
                        tile_type = self.map.tile_grid[row][col]

                        if tile_type != 0:
                            self.screen.blit(self.tile_textures.get(tile_type, self.BLACK), (iso_x, iso_y))
                        # draw a placeholder in case the texture is missing
                        else:
                            tile_rect = pygame.Rect(iso_x, iso_y, self.texture_size, self.texture_size)
                            pygame.draw.rect(self.screen, self.tile_colors.get(tile_type, self.BLACK), tile_rect)
                            pygame.draw.rect(self.screen, self.WHITE, tile_rect, 1)  # Grid outline
                    else:
                        # Draw background texture for out-of-bounds tiles
                        self.screen.blit(self.out_of_map_texture, (iso_x, iso_y))

            # when object is selected
            if self.object_selected:

                # highlight the selected object
                rect = pygame.Rect((self.selected_object_map_position_x * self.texture_size) + self.camera_x, (self.selected_object_map_position_y * self.texture_size) + self.camera_y, self.texture_size, self.texture_size)
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 5)

                # print detail view
                pygame.draw.rect(self.screen, self.LIGHT_GRAY, (0, self.game_screen_height-self.detail_view_height, self.detail_view_width, self.detail_view_height))
                text_surface = self.font.render(self.detail_view_text, True, self.BLACK)
                self.screen.blit(text_surface, (15, self.game_screen_height-self.detail_view_height+15))

            # print a bar in the top of the game showing the game stats
            s = pygame.Surface((self.game_screen_width, self.game_stats_bar_height), pygame.SRCALPHA)
            s.fill((*self.LIGHT_GRAY, 128))  # LIGHT_GRAY is (R, G, B)
            self.screen.blit(s, (0, 0))
            #pygame.draw.rect(self.screen, self.LIGHT_GRAY, (0, 0, self.game_screen_width, self.game_stats_bar_height))
            text_surface = self.font.render("Gold: "+str(self.game_stats.gold), True, self.BLACK)
            self.screen.blit(text_surface, (15, 10))

            # the following code is for moving the camera with WASD keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if self.camera_y < 0:
                    # the adjustments seems not to be needed for this move
                    test_camera_y = self.camera_y + self.scroll_speed
                    if test_camera_y > 0:
                        diff = 0 - abs(test_camera_y)
                        move = self.scroll_speed + diff
                        self.camera_y += move
                    else:
                        self.camera_y += self.scroll_speed
            if keys[pygame.K_a]:
                if self.camera_x < 0:
                    test_camera_x = self.camera_x + self.scroll_speed
                    if test_camera_x > 0:
                        diff = 0 - abs(test_camera_x)
                        move = self.scroll_speed + diff
                        self.camera_x += move
                    else:
                        self.camera_x += self.scroll_speed
            if keys[pygame.K_s]:
                if self.camera_y > -(self.max_move_up_down):
                    test_camera_y = self.camera_y - self.scroll_speed
                    if test_camera_y < -(self.max_move_up_down):
                        diff = abs(test_camera_y) - (self.max_move_up_down)
                        move = self.scroll_speed - diff
                        self.camera_y -= move
                    else:
                        self.camera_y -= self.scroll_speed
            if keys[pygame.K_d]:
                if self.camera_x > -(self.max_move_left_right):
                    test_camera_x = self.camera_x - self.scroll_speed
                    if test_camera_x < -(self.max_move_left_right):
                        diff = abs(test_camera_x) - (self.max_move_left_right)
                        move = self.scroll_speed - diff
                        self.camera_x -= move
                    else:
                        self.camera_x -= self.scroll_speed


            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_menu = True

                # perform some action based on which tile is currently pointed at by the mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print("map width:",self.map.get_map_tiles_width(), "map height:",self.map.get_map_tiles_height())
                    #print("self.mouse_map_position_x:",self.mouse_map_position_x,"self.mouse_map_position_y:",self.mouse_map_position_y)
                    if self.mouse_map_position_x < self.map.get_map_tiles_width() and self.mouse_map_position_x >= 0 and self.mouse_map_position_y < self.map.get_map_tiles_height() and self.mouse_map_position_y >= 0:
                        print(self.map.tile_grid[self.mouse_map_position_y][self.mouse_map_position_x])
                        if self.map.tile_grid[self.mouse_map_position_y][self.mouse_map_position_x] == 3:
                            self.object_selected = True
                            self.selected_object_map_position_x = self.mouse_map_position_x
                            self.selected_object_map_position_y = self.mouse_map_position_y
                            self.detail_view_text = "House. +5 gold every 10 seconds."
                        else:
                            self.object_selected = False
                            self.detail_view_text = ""

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.toggle_pause()
                    if event.key == pygame.K_ESCAPE:
                        self.in_menu = True
                    # the following code is for moving the camera with WASD keys
                    if event.key == pygame.K_w:
                        if self.camera_y < 0:
                            # the adjustments seems not to be needed for this move
                            test_camera_y = self.camera_y + self.scroll_speed
                            if test_camera_y > 0:
                                diff = 0 - abs(test_camera_y)
                                move = self.scroll_speed + diff
                                self.camera_y += move
                            else:
                                self.camera_y += self.scroll_speed
                    if event.key == pygame.K_a:
                        if self.camera_x < 0:
                            test_camera_x = self.camera_x + self.scroll_speed
                            if test_camera_x > 0:
                                diff = 0 - abs(test_camera_x)
                                move = self.scroll_speed + diff
                                self.camera_x += move
                            else:
                                self.camera_x += self.scroll_speed
                    if event.key == pygame.K_s:
                        if self.camera_y > -(self.max_move_up_down):
                            test_camera_y = self.camera_y - self.scroll_speed
                            if test_camera_y < -(self.max_move_up_down):
                                diff = abs(test_camera_y) - (self.max_move_up_down)
                                move = self.scroll_speed - diff
                                self.camera_y -= move
                            else:
                                self.camera_y -= self.scroll_speed
                    if event.key == pygame.K_d:
                        if self.camera_x > -(self.max_move_left_right):
                            test_camera_x = self.camera_x - self.scroll_speed
                            if test_camera_x < -(self.max_move_left_right):
                                diff = abs(test_camera_x) - (self.max_move_left_right)
                                move = self.scroll_speed - diff
                                self.camera_x -= move
                            else:
                                self.camera_x -= self.scroll_speed

            # Show the pause menu if the game is paused
            if self.paused:
                pause_menu = PauseMenu(self.screen, self.game_screen_width, self.game_screen_height)
                response = pause_menu.run()  # Pause menu blocks until resumed
                if response == "exit":
                    return "menu"
                else:
                    self.paused = False  # Unpause after returning from pause menu

            # Check if 10 seconds have passed
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= self.update_interval:
                num_houses = self.map.get_num_houses()
                gold_increase = num_houses * 5
                self.game_stats.gold += gold_increase  # Increase gold resource stat
                self.last_update_time = current_time  # Reset timer

            # DEBUG PRINTOUT only
            #print("Camera X,Y:", self.camera_x, self.camera_y)
            #print("Mouse X,Y:", self.mouse_x, self.mouse_y)
            #print("Mouse adjusted X,Y:", self.mouse_adjusted_x, self.mouse_adjusted_y)
            #print("Mouse map position X,Y:", self.mouse_map_position_x, self.mouse_map_position_y)

            # DEBUG: cord lines for help
            WHITE = (255, 255, 255)
            pygame.draw.line(self.screen, WHITE, (0, self.game_screen_height // 2), (self.game_screen_width, self.game_screen_height // 2), 1)
            pygame.draw.line(self.screen, WHITE, (self.game_screen_width // 2, 0), (self.game_screen_width // 2, self.game_screen_height), 1)


            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS

    def toggle_pause(self):
        """Toggles pause state."""
        self.paused = not self.paused
