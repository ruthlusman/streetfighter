import pygame
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.window_w, self.window_h = 1000, 564
        self.display = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("street fighter 3")
        self.clock = pygame.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill("white")
            self.all_sprites.draw(self.display)

            self.player.run(dt)

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
