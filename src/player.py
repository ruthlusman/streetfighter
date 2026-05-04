import pygame

def load_frames(path, frame_width, frame_height):
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width = sheet.get_width()
    frames = []

    for x in range(0, sheet_width, frame_width):
        frame = sheet.subsurface((x, 0, frame_width, frame_height))
        frames.append(frame)

    return frames

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.keys = None
        self.just_keys = None
        self.state = None

        self.SPEED = 300
        self.GRAVITY = 1200
        self.JUMP_HEIGHT = -500
        self.MAX_FALL_SPEED = 700
        self.can_jump = False
        self.velocity = pygame.math.Vector2(0,0)

        self.animations = {
            "idle": load_frames("../assets/ryu/stance.png", 78, 111),
            "walking": load_frames("../assets/ryu/walkf.png", 112, 113),
            "crouching": load_frames("../assets/ryu/crouching.png", 87, 73),
            "jumping": load_frames("../assets/ryu/jump.png", 86, 192),
            "light_punch": load_frames("../assets/ryu/far-lp.png", 121, 107),
            "light_kick": load_frames("../assets/ryu/far-lk.png", 122, 105),
            "medium_punch": load_frames("../assets/ryu/far-mp.png", 127, 105),
            "medium_kick": load_frames("../assets/ryu/far-mk.png", 154, 108),
            "heavy_punch": load_frames("../assets/ryu/far-hp.png", 130, 105),
            "heavy_kick": load_frames("../assets/ryu/hk.png", 153, 116),

        }
        self.frame_index = 0
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 1/4
        frames = self.animations["idle"]
        self.image = frames[self.frame_index]
        self.rect = self.image.get_rect(center=(500, 250))


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
            pygame.K_u: "heavy_punch",
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

    def animation(self):
        priority = [
            "heavy_punch", "heavy_kick",
            "medium_punch", "medium_kick",
            "light_punch", "light_kick",
            "jumping", "crouching", "walking", "idle"
        ]

        current_state = next((s for s in priority if s in self.state), "idle")

        if current_state != getattr(self, "_last_state", None):
            self.frame_index = 0
            self.animation_timer = 0
            self._last_state = current_state

        frames = self.animations[current_state]

        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        self.image = frames[self.frame_index]
        self.rect = self.image.get_rect(center = self.rect.center)

    def input(self, dt):
        # walking
        self.velocity.x = int(self.keys[pygame.K_d]) - int(self.keys[pygame.K_a])
        self.rect.x += self.velocity.x * self.SPEED * dt

        self.velocity.y += self.GRAVITY * dt
        self.rect.y += self.velocity.y * dt
        if "jumping" in self.state and self.can_jump: self.velocity.y = self.JUMP_HEIGHT; self.can_jump = False
        if self.velocity.y >= self.MAX_FALL_SPEED: self.velocity.y = self.MAX_FALL_SPEED

    def run(self, dt):
        self.state_machine()
        self.input(dt)
        self.animation()
