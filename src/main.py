import pygame
from player import Player
from ground import Ground

class Game:
    def __init__(self):
        pygame.init()
        self.window_w, self.window_h = 1000, 564
        self.display = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("street fighter 3")
        self.clock = pygame.Clock()
        self.running = True

        # groups
        self.all_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player(self.all_sprites)
        self.ground = Ground(self.all_sprites)

    def ground_collisions(self):
        collision = pygame.sprite.collide_rect(self.player, self.ground)
        if collision and self.player.velocity.y >= 0:
            self.player.rect.bottom = self.ground.rect.top
            self.player.can_jump = True
            self.player.velocity.y = 0

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill("white")
            self.all_sprites.draw(self.display)

            self.player.run(dt)
            self.ground_collisions()

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
