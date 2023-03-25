from pygame import *
from map import *
mixer.init()
window = display.set_mode((700, 600))
display.set_caption("Лабіринт")
background = transform.scale(image.load("resources/background.jpg"), (700, 600))
window.blit(background, (0, 0))
musik = mixer.music.load("resources/jungles.ogg")
# mixer.music.play()
kick = mixer.Sound("resources/kick.ogg")
money = mixer.Sound("resources/money.ogg")
clock = time.Clock()
game = True


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_w] and self.rect.y >= 0:
            self.rect.y -= self.speed
        if pressed_keys[K_s] and self.rect.y + self.rect.height <= 580:
            self.rect.y += self.speed
        if pressed_keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if pressed_keys[K_d] and self.rect.x + self.rect.height <= 700:
            self.rect.x += self.speed

    def is_touch(self, sprite_ob):
        return self.rect.colliderect(sprite_ob.rect)


class Enemy(GameSprite):

    def update(self, x1, x2):
        self.rect.x += self.speed
        if self.rect.x <= x1 or self.rect.x + self.rect.width >= x2:
            self.speed *= -1


hero = Player('resources/hero.png', 0, 0, 5)
hero.draw_sprite()
cyborg = Enemy('resources/cyborg.png', 350, 200, 2)
cyborg.draw_sprite()
treasure = GameSprite('resources/treasure.png', 550, 400)
treasure.draw_sprite()

game_map = make_map()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    hero.update()
    cyborg.update(350, 550)
    if hero.is_touch(cyborg):
        kick.play()
        hero.rect.x = 0
        hero.rect.y = 0
    if hero.is_touch(treasure):
        print("You Won")
        break
    window.blit(background, (0, 0))
    for block in game_map:
        draw.rect(window, (134,10,50), block)
        if hero.rect.colliderect(block):
            hero.rect.x = 0
            hero.rect.y = 0

    hero.draw_sprite()
    cyborg.draw_sprite()
    treasure.draw_sprite()
    display.update()
    clock.tick(60)
