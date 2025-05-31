import pygame
import pygame_gui

from game_enums import WindowMode

class Settings:
    def __init__(self, screen, WIDTH, HEIGHT, resolutions_list, game_settings, FPS_COUNTER, REFRESH_RATE):
        self.screen = screen
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.game_screen_width = WIDTH
        self.game_screen_height = HEIGHT
        self.FPS_COUNTER = FPS_COUNTER
        self.REFRESH_RATE = REFRESH_RATE
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)
        self.game_settings = game_settings
        self.game_resolution = self.game_settings.resolution
        self.game_resolution_string = f"{self.game_resolution[0]}x{self.game_resolution[1]}"
        self.resolutions_list = resolutions_list
        self.resolution_strings = [f"{w}x{h}" for w, h in self.resolutions_list]
        self.window_mode = self.game_settings.window_mode
        self.window_modes_list = [mode.value for mode in WindowMode]
        self.window_mode_string = str(self.window_mode.value)
        
        self.window_mode_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.window_modes_list,
            starting_option=self.window_mode_string,
            relative_rect=pygame.Rect((400, 150), (200, 30)),
            manager=self.manager
        )
        
        self.resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.resolution_strings,
            starting_option=self.game_resolution_string,
            relative_rect=pygame.Rect((400, 250), (200, 30)),
            manager=self.manager
        )

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 350), (200, 60)),
            text='Back',
            manager=self.manager
        )
    
    def draw(self):
        self.screen.fill((40, 40, 40))

        # Settings Title
        font = pygame.font.Font(None, 50)
        text = font.render("Settings - Press ESC to go back", True, (255, 255, 255))
        self.screen.blit(text, (100, 50))

        label_text = font.render("Window Mode:", True, (255, 255, 255))
        self.screen.blit(label_text, (100, 150))
        
        label_text = font.render("Resolution:", True, (255, 255, 255))
        self.screen.blit(label_text, (100, 250))

        # Draw the UI elements (Dropdown and Buttons)
        self.manager.draw_ui(self.screen)

        if self.FPS_COUNTER:
            font = pygame.font.SysFont(None, 24)
            fps = self.clock.get_fps()
            fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
            self.screen.blit(fps_text, (self.game_screen_width-100, 10))

        pygame.display.flip()
        self.clock.tick(self.REFRESH_RATE)  # Limit the FPS to set system refresh rate

    def handle_event(self, event):
        """Handle keyboard input for settings screen"""
        
        if event.type == pygame.QUIT:
            return "back_to_menu"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back_to_menu"  # Go back to the main menu  
                
        # Process pygame_gui events (buttons, dropdowns, etc.)
        self.manager.process_events(event)

        if self.back_button.check_pressed():
            return "back_to_menu"  # Return to the main menu
        
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.resolution_dropdown:
                self.game_resolution_string = event.text
                index = self.resolution_strings.index(self.game_resolution_string)
                self.game_resolution = self.resolutions_list[index]
                self.game_settings.resolution = self.game_resolution
                self.game_settings.save_resolution_to_json()
                
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.window_mode_dropdown:
                self.window_mode_string = event.text
                index = self.window_modes_list.index(self.window_mode_string)
                if self.window_modes_list[index] == "FULL_SCREEN":
                    self.window_mode = WindowMode.FULL_SCREEN
                elif self.window_modes_list[index] == "WINDOWED":
                    self.window_mode =  WindowMode.WINDOWED
                elif self.window_modes_list[index] == "BORDERLESS":
                    self.window_mode = WindowMode.BORDERLESS
                else:
                    self.window_mode = WindowMode.WINDOWED
                self.game_settings.window_mode = self.window_mode
                self.game_settings.save_window_mode_to_json()

        return None

    def get_selected_window_mode(self):
        """Returns the selected window mode from the dropdown"""
        return self.window_mode_dropdown.selected_option