import pygame
import pygame_gui

from game_enums import WindowMode

class Settings:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 50)
        self.selected_index = 0
        #self.options = ["Full Screen", "Window Mode"]
        self.current_mode = 0  # Default to "Full Screen"
        
        self.window_modes_list = [mode.value for mode in WindowMode]
        
        self.window_mode_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.window_modes_list,
            starting_option=self.window_modes_list[0],  # Default to "Full Screen"
            relative_rect=pygame.Rect((400, 150), (200, 30)),
            manager=self.manager
        )

        # Back button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 250), (200, 60)),
            text='Back',
            manager=self.manager
        )
    
    def draw(self):
        self.screen.fill((40, 40, 40))

        # Settings Title
        font = pygame.font.Font(None, 50)
        text = font.render("Settings - Press ESC to go back", True, (255, 255, 255))
        self.screen.blit(text, (100, 50))

        # "Window Mode" label (for the dropdown)
        label_text = font.render("Window Mode:", True, (255, 255, 255))
        self.screen.blit(label_text, (100, 150))

        # Draw the UI elements (Dropdown and Buttons)
        self.manager.draw_ui(self.screen)

        pygame.display.flip()

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

        return None

    def get_selected_window_mode(self):
        """Returns the selected window mode from the dropdown"""
        return self.window_mode_dropdown.selected_option