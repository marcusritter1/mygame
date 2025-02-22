import pygame
from pause import PauseMenu
from quit_popup import QuitPopup

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.paused = False
        self.x_pos = 100  # Starting position of the animated object (circle)
        self.y_pos = 100
        self.x_velocity = 5  # Speed of the animation (movement per frame)
        self.y_velocity = 3  # Vertical speed of the animation

    def run(self):
        while self.running:
            self.screen.fill((0, 100, 200))  # Game background color

            # Create a simple animated object (moving circle)
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x_pos, self.y_pos), 20)

            # Update the position of the circle to create animation
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity

            # Bounce the circle off the walls
            if self.x_pos >= self.screen.get_width() - 20 or self.x_pos <= 20:
                self.x_velocity = -self.x_velocity  # Reverse horizontal direction
            if self.y_pos >= self.screen.get_height() - 20 or self.y_pos <= 20:
                self.y_velocity = -self.y_velocity  # Reverse vertical direction

            pygame.display.flip()

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

