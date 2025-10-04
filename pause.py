import pygame
from ingame_menu import InGameMenu

class PauseMenu:
    def __init__(self, screen, game_screen_width, game_screen_height, FPS_COUNTER, REFRESH_RATE):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()
        self.game_screen_width = game_screen_width
        self.game_screen_height = game_screen_height
        self.FPS_COUNTER = FPS_COUNTER
        self.REFRESH_RATE = REFRESH_RATE

        # time counter for fps display, to draw it only every second
        self.last_fps_update = 0
        self.fps_font = pygame.font.SysFont(None, 24)
        self.fps_text = self.fps_font.render("FPS: 0/0", True, (255, 255, 255))

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

            if self.FPS_COUNTER:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_fps_update > 500:
                    self.last_fps_update = current_time
                    fps = self.clock.get_fps()
                    self.fps_text = self.fps_font.render(f"FPS: {fps:.0f}/{self.REFRESH_RATE}", True, (255, 255, 255))
                self.screen.blit(self.fps_text, (self.game_screen_width-120, 10))

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
    
                if event.type == pygame.KEYDOWN:
                    # activate/deactivate fps counter
                    if event.key == pygame.K_F1:
                        self.FPS_COUNTER = not self.FPS_COUNTER
            
            self.clock.tick(self.REFRESH_RATE)  # Limit to 60 FPS
