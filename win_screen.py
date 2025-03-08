import pygame
import pygame_gui

class WinScreen:

    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 50)

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 350), (200, 60)),
            text='Back to menu',
            manager=self.manager
        )
    
    def draw(self):
        self.screen.fill((40, 40, 40))

        font = pygame.font.Font(None, 50)
        text = font.render("You won the game!", True, (255, 255, 255))
        self.screen.blit(text, (100, 50))

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
    