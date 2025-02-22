import pygame
from quit_popup import QuitPopup

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)

    def run(self):
        # Capture the current screen contents (game background)
        background = self.screen.copy()

        # Transparent black overlay (alpha = 150)
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Transparent black with alpha (semi-transparent)

        paused_text = self.font.render("Paused - Press P to Resume", True, (255, 255, 255))

        while True:
            # Blit the captured background (game content) onto the screen
            self.screen.blit(background, (0, 0))  # Draw the original game background
            self.screen.blit(overlay, (0, 0))  # Draw the transparent overlay
            self.screen.blit(paused_text, (200, 250))  # Draw the paused text

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_popup = QuitPopup(self.screen)
                    response = quit_popup.wait_for_response()
                    if response == "Yes":
                        return "exit"  # Signal to exit to the main menu
                    elif response == "No":
                        pass
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    return  # Unpause and return to the game
