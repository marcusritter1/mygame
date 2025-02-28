import pygame
from ingame_menu import InGameMenu

class PauseMenu:
    def __init__(self, screen, game_screen_width, game_screen_height):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()
        self.game_screen_width = game_screen_width
        self.game_screen_height = game_screen_height

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
                    game_menu = InGameMenu(self.screen, self.game_screen_width, self.game_screen_height)
                    response = game_menu.wait_for_response()
                    if response == "exit":
                        return "exit"
                    elif response == "continue":
                        pass
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    return  # Unpause and return to the game
            
            self.clock.tick(60)  # Limit to 60 FPS
