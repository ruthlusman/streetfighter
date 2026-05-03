import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.keys = None
        self.just_keys = None
        self.state = None
        self.image = pygame.Surface((50, 150))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center = (250, 300))
        self.SPEED = 300
        self.velocity = pygame.math.Vector2(0,0)

    def state_machine(self):
        self.keys = pygame.key.get_pressed()
        self.just_keys = pygame.key.get_just_pressed()
        movement_states = {             # this is for button presses that can be held
            pygame.K_a: "walking",
            pygame.K_d: "walking",
            pygame.K_s: "crouching",
        }
        button_states = {               # this is for button presses that only last one frame
            pygame.K_w: "jumping",
            pygame.K_t: "light_punch",
            pygame.K_y: "medium_punch",
            pygame.K_u: "heavy punch",
            pygame.K_g: "light_kick",
            pygame.K_h: "medium_kick",
            pygame.K_j: "heavy_kick",
        }
        self.state = set()
        for key, state in movement_states.items():
            if self.keys[key]:
                self.state.add(state)

        for key, state in button_states.items():
            if self.just_keys[key]:
                self.state.add(state)

        if not self.state:
            self.state.add("idle")

    def input(self, dt):
        # walking
        self.velocity.x = int(self.keys[pygame.K_RIGHT]) - int(self.keys[pygame.K_LEFT])
        self.rect.x += self.velocity.x * self.SPEED * dt

    def run(self, dt):
        self.state_machine()
        self.input(dt)
        print(self.state)
