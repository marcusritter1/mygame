import pygame

class QuitPopup:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.options = ["Yes", "No"]
        self.selected_index = 1  # Default to "No" to avoid accidental quits

    def draw(self):
        """Render the quit confirmation menu."""
        self.screen.fill((50, 50, 50))  # Dark gray background

        # Render the question
        question_text = self.font.render("Do you really want to quit?", True, (255, 255, 255))
        self.screen.blit(question_text, (200, 200))

        # Render options
        for index, text in enumerate(self.options):
            color = (255, 255, 255) if index != self.selected_index else (255, 0, 0)
            option_text = self.font.render(text, True, color)
            self.screen.blit(option_text, (350, 300 + index * 60))

        pygame.display.flip()

    def handle_event(self, event):
        """Handle user input for quit confirmation."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]  # Return "Yes" or "No"
        return None

    def wait_for_response(self):
        """Wait for the user to choose Yes or No."""
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Yes"  # Auto-quit if window is closed
                response = self.handle_event(event)
                if response == "Yes":
                    return "Yes"
                elif response == "No":
                    return "No"
                else:
                    pass
