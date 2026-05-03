import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((1000, 130))
        self.image.fill("green")
        self.rect = self.image.get_rect(bottomleft = (0, 564))
