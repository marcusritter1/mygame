import pygame
import pygame_gui
from save_games import SaveGame

class InGameMenu:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 50)
        self.options = ["continue", "save_game", "exit"]
        self.selected_index = 0

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 150), (200, 60)),
            text='Continue',
            manager=self.manager
        )
        
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 250), (200, 60)),
            text='Save game',
            manager=self.manager
        )
        
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 350), (200, 60)),
            text='Exit',
            manager=self.manager
        )
        
        self.buttons = [self.continue_button, self.save_button, self.exit_button]
        self.highlight_selected()

    def draw(self):
        """Render the quit confirmation menu."""
        self.screen.fill((30, 30, 30))  # Dark gray background

        # Draw the UI elements (Dropdown and Buttons)
        self.manager.draw_ui(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        """Handle user input for quit confirmation."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.highlight_selected()
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.highlight_selected()
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]  # Return "Yes" or "No"
            
        # Process pygame_gui events (buttons, dropdowns, etc.)
        self.manager.process_events(event)

        if self.continue_button.check_pressed():
            return "continue"

        if self.save_button.check_pressed():
            return "save_game"

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


    def wait_for_response(self, game_stats):
        while True:
            time_delta = pygame.time.Clock().tick(60) / 1000.0  # Frame rate
            self.manager.update(time_delta)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"  # Auto-quit if window is closed
                response = self.handle_event(event)
                if response == "continue":
                    return "continue"
                elif response == "exit":
                    return "exit"
                elif response == "save_game":
                    self.save_game = SaveGame(game_stats=game_stats)
                    self.save_game.save_savegame()
                else:
                    pass
