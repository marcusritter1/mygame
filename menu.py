import pygame
from quit_popup import QuitPopup
import pygame_gui

class Menu:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 50)
        self.options = ["Start", "Settings", "Exit"]
        self.selected_index = 0
        
        # Start button
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 150), (200, 60)),
            text='Start',
            manager=self.manager
        )
        
        # Settings button
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 250), (200, 60)),
            text='Settings',
            manager=self.manager
        )
        
        # Exit button
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 350), (200, 60)),
            text='Exit',
            manager=self.manager
        )
        
        self.buttons = [self.start_button, self.settings_button, self.exit_button]
        self.highlight_selected()

    def draw(self):
        """Render the main menu."""
        self.screen.fill((30, 30, 30))  # Dark background
            
        # Draw the UI elements (Dropdown and Buttons)
        self.manager.draw_ui(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        """Handle keyboard navigation and selection."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.highlight_selected()
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.highlight_selected()
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected_index] == "Start":
                    return "start"
                elif self.options[self.selected_index] == "Settings":
                    return "settings"
                elif self.options[self.selected_index] == "Exit":
                    return "exit"
        
        # Process pygame_gui events (buttons, dropdowns, etc.)
        self.manager.process_events(event)

        if self.start_button.check_pressed():
            return "start"

        if self.settings_button.check_pressed():
            return "settings"

        if self.exit_button.check_pressed():
            return "exit"    
        
        return None
    
    def highlight_selected(self):
        """Change button colors to indicate selection."""
        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                button.set_text(f"> {button.text} <")  # Highlight selected button
            else:
                button.set_text(button.text.replace("> ", "").replace(" <", ""))
