import random
import pygame
import os
import time
import mouse
from screeninfo import get_monitors

window_size = (800, 600)
monitor = get_monitors()[0]
window_size = (monitor.width, monitor.height)
screen = pygame.display.set_mode(window_size)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")
pygame.mouse.set_visible(False)

x = window_size[0] // 2 - 25
y = window_size[1] // 2 - 50
pleyer = pygame.Rect(x, y, 50, 100)
pleyer_detecsen = pygame.Rect(x-1000, y-1000, 1000, 1000)
speed = 0.15
sprint_speed = 0.8
sprint_time = 5
sprinting = False
sprinting_cooldown = 0.5
time_last_sprint = time.time()
en_x = 0
en_y = 0

flower_dir = os.path.join("plants", "flowers")
flowers = []

for filename in os.listdir(flower_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(flower_dir, filename)
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (50, 50))
        flowers.append(img)

grass_dir = os.path.join("plants", "grass")
grasses = []

def get_screenshake_offset(intensity):
    return (
        random.randint(-intensity, intensity),
        random.randint(-intensity, intensity)
    ) if intensity > 0 else (0, 0)
shake_intensity = 0
shake_time = 0



for filename in os.listdir(grass_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(grass_dir, filename)
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (50, 50))
        grasses.append(img)

class partical:
    def __init__(self, x, y, r, g, b,lifspand = random.randint(50, 100),speed = 0.1):
        self.r = r
        self.g = g
        self.b = b
        self.x = x
        self.y = y
        self.lifspand = lifspand
        self.dir_x = random.uniform(-1, 1)
        self.dir_y = random.uniform(-1, 1)
        self.speed = speed
        self.radius = 2
        self.color = (r, g, b)

    def update(self, screen, env_x, env_y):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.x -= env_x
        self.y -= env_y
        self.lifspand -= 1
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
particals = []
class basic_enemy:
    def __init__(self):
        global envirement_x,envirement_y
        self.life = 100
        self.max_life = 100
        self.x = random.randint(-300, window_size[0] + 300)
        self.y = random.randint(-300, window_size[1] + 300)
        self.rect = pygame.Rect(self.x, self.y, 50, 100)
        self.life_rect = pygame.Rect(self.x, self.y - 10, 50 * (self.life / self.max_life), 5)
        self.life_color = (255, 0, 0)
        self.speed = 1
        self.coler = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.last_shoted = time.time()
        self.corent_time = time.time()
        self.deley = random.randint(5,30)
        self.deley = self.deley/10 if random.randint(1,15) == 2 else 0.1
    def update(self, screen, ofset_x=0, ofset_y=0):
        self.x -= ofset_x
        self.y -= ofset_y
        self.corent_time = time.time()
        if self.rect.colliderect(pleyer_detecsen):
            if self.corent_time - self.last_shoted > self.deley:
                if random.randint(1,100) == 7:
                    player_centerx = pleyer.centerx
                    player_centery = pleyer.centery
                    enemy_centerx = self.x + 25
                    enemy_centery = self.y + 50
                    dir_x = player_centerx - enemy_centerx + ((random.randint(1,20)-1)*10)
                    dir_y = player_centery - enemy_centery + ((random.randint(1,20)-1)*10)
                    length = max(1, (dir_x ** 2 + dir_y ** 2) ** 0.5)
                    dir_x /= length
                    dir_y /= length
                    bullets.append(Bullet(enemy_centerx, enemy_centery, dir_x , dir_y,2))
                    self.last_shoted = self.corent_time
        self.rect = pygame.Rect(self.x, self.y, 50, 100)
        pygame.draw.rect(screen, self.coler, self.rect)
        self.life_rect = pygame.Rect(self.x, self.y - 10, 50 * (self.life / self.max_life), 5)
        if self.life <= 0:
            self.life_rect.width = 0
        else:
            self.life_rect.width = 50 * (self.life / 100)
        pygame.draw.rect(screen, self.life_color, self.life_rect)


class palants:
    def __init__(self):
        self.x = random.randint(-1000, window_size[0] + 1000)
        self.y = random.randint(-1000, window_size[1] + 1000)
        self.plant_type = random.choice(flowers)
    def update(self, screen, ofset_x=0, ofset_y=0):
        self.x -= ofset_x
        self.y -= ofset_y
        screen.blit(self.plant_type, (self.x, self.y))

class grass:
    def __init__(self):
        self.x = random.randint(-1000, window_size[0] + 1000)
        self.y = random.randint(-1000, window_size[1] + 1000)
        self.plant_type = random.choice(grasses)
    def update(self, screen, ofset_x=0, ofset_y=0):
        self.x -= ofset_x
        self.y -= ofset_y
        screen.blit(self.plant_type, (self.x, self.y))

class Bullet:
    def __init__(self, x, y, dir_x, dir_y,tipe):
        self.life = 150
        self.tipe = tipe
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = 3
        self.radius = 5
        self.color = (255, 255, 0) if self.tipe == 1 else (255, 50, 50)

    def update(self, screen, env_x, env_y):
        self.life -= 5
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.x -= env_x
        self.y -= env_y
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        for i in range(self.life):
            particals.append(partical(self.x, self.y, 255, 255, 0,lifspand=random.randint(1, 20)))
bullets = []

grass_list = []
for i in range(150):
    grass_list.append(grass())
plants = [palants() for i in range(250)]

def draw_cooldown_bar(screen, x, y, width, height, progress, border_color=(255, 255, 255), fill_color=(0, 255, 0)):
    pygame.draw.rect(screen, border_color, (x, y, width, height), 2)
    inner_width = (width - 4) * progress
    pygame.draw.rect(screen, fill_color, (x + 2, y + 2, inner_width, height - 4))


envirement_x = 0
envirement_y = 0
enimies = []
for i in range(10):
    enimies.append(basic_enemy())

pygame.init()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dir_x = mouse_x - pleyer.centerx
            dir_y = mouse_y - pleyer.centery
            length = max(1, (dir_x ** 2 + dir_y ** 2) ** 0.5)
            dir_x /= length
            dir_y /= length
            bullets.append(Bullet(pleyer.centerx + envirement_x, pleyer.centery + envirement_y, dir_x, dir_y,1))
    screen.fill((96, 151, 50))
    pleyer = pygame.Rect(x, y, 50, 100)
    pleyer_detecsen = pygame.Rect(x-1000, y-1000, 1000, 1000)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        envirement_x -= speed if not sprinting else sprint_speed
    if keys[pygame.K_RIGHT]or keys[pygame.K_d]:
        envirement_x += speed if not sprinting else sprint_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        envirement_y -= speed if not sprinting else sprint_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        envirement_y += speed if not sprinting else sprint_speed
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_SPACE]:
        if sprint_time > 0:
            sprinting = True
            sprint_time -= 0.06
        else:
            sprinting = False
            if time_last_sprint == 0:
                time_last_sprint = time.time()
    else:
        sprinting = False


        if sprint_time <= 0 and time.time() - time_last_sprint > sprinting_cooldown:
            sprint_time = 5.0
            time_last_sprint = 0
    if shake_time > 0:
        offset_x, offset_y = get_screenshake_offset(shake_intensity)
        shake_time -= 1
    else:
        offset_x, offset_y = 0, 0
        pleyer.x = window_size[0] // 2 - 25 + envirement_x
        pleyer.y = window_size[1] // 2 - 50 + envirement_y
    en_x -= envirement_x
    en_y -= envirement_y
    if en_x > 1500:
        envirement_x = 0
    if en_y > 1500:
        envirement_y = 0
    if en_x < -1500:
        envirement_x = 0
    if en_y < -1500:
        envirement_y = 0

    for grass_i in grass_list:
        grass_i.update(screen, envirement_x + offset_x, envirement_y + offset_y)
    for plant in plants:
        plant.update(screen, envirement_x + offset_x, envirement_y + offset_y)
    for enemy in enimies:
        enemy.update(screen, envirement_x + offset_x, envirement_y + offset_y)
    for partical_i in particals:
        partical_i.update(screen, envirement_x + offset_x, envirement_y + offset_y)
        if partical_i.lifspand <= 0:
            particals.remove(partical_i)
    for bullet in bullets[:]:
        bullet.update(screen, envirement_x + offset_x, envirement_y + offset_y)

        if bullet.x < -2000 or bullet.x > 2000 or bullet.y < -2000 or bullet.y > 2000:
            bullets.remove(bullet)
        if bullet.tipe == 1:
            for enemy in enimies[:]:
                if enemy.rect.colliderect(pygame.Rect(bullet.x - envirement_x + offset_x, bullet.y - envirement_y + offset_y, bullet.radius * 2, bullet.radius * 2)):
                    for _ in range(10):
                        particals.append(partical(bullet.x, bullet.y, 255, 255, 0))
                    bullets.remove(bullet)

                    enemy.life -= 40
                    if enemy.life <= 0:
                        for _ in range(400):
                            particals.append(partical(random.randint(int(enemy.x),int(enemy.x)+50), random.randint(int(enemy.y),int(enemy.y)+100), 150, 0, 0,lifspand=random.randint(50, 500), speed=2.01))
                        enemy.color = (255, 0, 0)
                        enimies.remove(enemy)
                        shake_intensity = 1
                        shake_time = 100
                        enimies.append(basic_enemy())
                    break
        elif 2:
            if pleyer.colliderect(pygame.Rect(bullet.x - envirement_x + offset_x, bullet.y - envirement_y + offset_y, bullet.radius * 2, bullet.radius * 2)):
                for _ in range(10):
                    particals.append(partical(bullet.x, bullet.y, 255, 255, 0))
                bullets.remove(bullet)
                shake_time = 150

    x = (window_size[0] // 2 - 25) + offset_x
    y = (window_size[1] // 2 - 50) + offset_y
    #envirement_x = envirement_x if envirement_x < 

    pygame.draw.rect(screen, (255, 0, 0), pleyer)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    world_mouse_x = mouse_x + envirement_x
    world_mouse_y = mouse_y + envirement_y
    world_mouse_pos = (mouse_x + envirement_x, mouse_y + envirement_y)

    pygame.draw.circle(screen, (0, 0, 255), (mouse_x, mouse_y), 5)  
    pygame.draw.circle(screen, (255, 0, 255), (world_mouse_pos[0] - envirement_x, world_mouse_pos[1] - envirement_y), 5)

    envirement_y = (envirement_y / 1.05)
    envirement_x = (envirement_x / 1.05)
    
    bar_width = 200
    bar_height = 20
    bar_x = window_size[0] - bar_width - 20 
    bar_y = window_size[1] - bar_height - 20 
    
    if sprint_time > 0:
        progress = sprint_time / 5.0  
        color = (0, 255, 0) 
    else:
        progress = min(1.0, (time.time() - time_last_sprint) / sprinting_cooldown)
        color = (255, 165, 0) 
    
    draw_cooldown_bar(screen, bar_x, bar_y, bar_width, bar_height, progress, fill_color=color)
    
    pygame.display.flip()
pygame.quit()
