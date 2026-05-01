import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.valid_keys = []
        self.keys = None
        self.image = pygame.Surface((50, 150))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center = (250, 300))
        self.state = "idle"
        self.SPEED = 300
        self.velocity = pygame.math.Vector2(0,0)

    def state_machine(self):
        self.keys = pygame.key.get_pressed()
        self.valid_keys = [pygame.K_LEFT, pygame.K_RIGHT]
        for key in self.valid_keys:
            if not self.keys[key]:
                if self.velocity.x != 0:
                    self.state = "walking"
                else:
                    self.state = "idle"

    def input(self, dt):
        # walking
        self.velocity.x = int(self.keys[pygame.K_RIGHT]) - int(self.keys[pygame.K_LEFT])
        self.rect.x += self.velocity.x * self.SPEED * dt

    def run(self, dt):
        self.state_machine()
        self.input(dt)
        print(self.state)
