import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, text="Click",
                 pos=(0, 0), fontsize=16,
                 colors="white on blue",
                 # hover_colors="red on green",
                 command=lambda:
                 print("No command activated for this button")):
        super().__init__()
        self.text = text
        self.command = command
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        self.font = pygame.font.SysFont("Arial", fontsize)
        self.pos = pos
        self.set_text(self.text)

    def create_bg(self, text, fg, bg):
        self.text = text
        image = self.font.render(self.text, 1, fg)
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = self.pos

        bgo = pygame.Surface((self.rect.w, self.rect.h))
        bgo.fill(bg)
        bgo.blit(image, (0, 0))
        return bgo

    def set_text(self, text):
        self.image = self.create_bg(text, self.fg, self.bg)
        self.original_image = self.image.copy()

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and \
            pygame.mouse.get_pressed()[0]
