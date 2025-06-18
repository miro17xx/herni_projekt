import pygame
import math
import random
from sys import exit

sirka = 1900
vyska = 1020
FPS = 60

hrac_start_x = 300
hrac_start_y = 200
hrac_size1 = 0.45
hrac_speed = 8
hrac_max_health = 100

z_size = 0.33
z_start_speed = 1
z_max_speed = 6.1
z_spawn_interval = 900

s_scale = 1.5
s_cool = 25
s_etime = 750

powerup_duration = 4500  

gun_offset_x = 20
gun_offset_y = -5


kills = 0

pygame.init()
screen = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption("Zombik Shooter")
clock = pygame.time.Clock()

pozadi = pygame.transform.scale(pygame.image.load("obrazky/background1.png").convert(), (sirka, vyska))
font = pygame.font.SysFont(None, 50)



class Hrac(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_player_image = pygame.transform.rotozoom(pygame.image.load("obrazky/hrac3.png").convert_alpha(), 0, hrac_size1)
        self.image = self.base_player_image
        self.pos = pygame.math.Vector2(hrac_start_x, hrac_start_y)
        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = hrac_speed
        self.shoot = False
        self.shoot_cooldown = 0
        self.gun_offset = pygame.math.Vector2(gun_offset_x, gun_offset_y)
        self.health = hrac_max_health
        self.max_health = hrac_max_health
        self.recoil_cooldown = 0
        self.recoil = 25
        self.recoil_effect_active = False
        self.recoil_timer = 0

    def hrac_rotation(self):
        self.mys_coords = pygame.mouse.get_pos()
        self.x_mys_change = (self.mys_coords[0] - self.hitbox_rect.centerx)
        self.y_mys_change = (self.mys_coords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_mys_change, self.x_mys_change))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)









    

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed

        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.shoot = True
            self.shooting()
        else:
            self.shoot = False

    def shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.recoil
            spawn_strela_pos = self.pos + self.gun_offset.rotate(self.angle)
            strela = Strela(spawn_strela_pos[0], spawn_strela_pos[1], self.angle)
            Strela_group.add(strela)
            Vsechny_sprites_group.add(strela)

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

        player_width = self.rect.width
        player_height = self.rect.height

        self.pos.x = max(player_width // 2, min(sirka - player_width // 2, self.pos.x))
        self.pos.y = max(player_height // 2, min(vyska - player_height // 2, self.pos.y))

        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.hrac_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.recoil_effect_active:
            now = pygame.time.get_ticks()
            if now - self.recoil_timer >= powerup_duration:
                self.recoil_effect_active = False
                self.recoil = s_cool

    def draw_health_bar(self, surface):
        bar_x = 10
        bar_y = 10
        bar_width = 200
        bar_height = 20
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, int(bar_width * ratio), bar_height))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)

class Strela(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("obrazky/strela.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, s_scale)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.angle = angle
        s_speed = 20
        self.x_vel = math.cos(math.radians(self.angle)) * s_speed
        self.y_vel = math.sin(math.radians(self.angle)) * s_speed
        self.s_lifetime = s_etime
        self.spawn_time = pygame.time.get_ticks()

    def Strela_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if pygame.time.get_ticks() - self.spawn_time > self.s_lifetime:
            self.kill()

    def update(self):
        self.Strela_movement()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.base_image = pygame.image.load("obrazky/zombie.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.base_image, 0, z_size)
        self.rect = self.image.get_rect(center=position)
        self.pos = pygame.math.Vector2(position)
        self.speed = z_start_speed
        self.health = 3
        self.max_health = 3
        self.angle = 0

    
    def update(self):
        direction = player.pos - self.pos
        if direction.length() != 0:
            direction = direction.normalize()
        self.pos += direction * self.speed
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.angle = math.degrees(math.atan2(direction.y, direction.x))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.image = pygame.transform.rotozoom(self.image, 0, z_size)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.speed > z_max_speed:
            self.speed = z_max_speed
        if self.health <= 0:
            self.kill()

    def draw_health_bar(self, surface):
        bar_width = 40
        bar_height = 5
        ratio = self.health / self.max_health
        bar_x = self.rect.left
        bar_y = self.rect.top - 10
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, int(bar_width * ratio), bar_height))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, typ):
        super().__init__()
        self.type = typ
        self.image = pygame.image.load("obrazky/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        pass

Vsechny_sprites_group = pygame.sprite.Group()
Strela_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

player = Hrac()
Vsechny_sprites_group.add(player)

spawn_zombik = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_zombik, z_spawn_interval)

spawn_powerup = pygame.USEREVENT + 2
next_powerup_spawn = random.randint(15000, 25000)
pygame.time.set_timer(spawn_powerup, next_powerup_spawn)

running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == spawn_zombik:
            spawn_x = random.randint(0, sirka)
            spawn_y = random.randint(0, vyska)
            new_zombie = Enemy((spawn_x, spawn_y))
            for z in enemy_group:
                z.speed = min(z.speed + 0.1, z_max_speed)
            new_zombie.speed = z_start_speed
            enemy_group.add(new_zombie)
            Vsechny_sprites_group.add(new_zombie)
        elif event.type == spawn_powerup:
            spawn_x = random.randint(50, sirka - 50)
            spawn_y = random.randint(50, vyska - 50)
            power_type = random.choice(['heal', 'recoil'])
            powerup = PowerUp((spawn_x, spawn_y), power_type)
            powerup_group.add(powerup)
            Vsechny_sprites_group.add(powerup)
            next_powerup_spawn = random.randint(15000, 25000)
            pygame.time.set_timer(spawn_powerup, next_powerup_spawn)

    Vsechny_sprites_group.update()

    for strela in Strela_group:
        hit_zombies = pygame.sprite.spritecollide(strela, enemy_group, False)
        for zombie in hit_zombies:
            zombie.health -= 1
            strela.kill()
            if zombie.health <= 0:
                kills += 1  

    hit_by_zombies = pygame.sprite.spritecollide(player, enemy_group, False)
    for zombie in hit_by_zombies:
        player.health -= 0.25
        if player.health < 0:
            player.health = 0
        push_vec = player.pos - zombie.pos
        if push_vec.length() != 0:
            push_vec = push_vec.normalize()
        player.pos += push_vec * 5
        player.hitbox_rect.center = player.pos
        player.rect.center = player.hitbox_rect.center

    powerup_hits = pygame.sprite.spritecollide(player, powerup_group, True)
    for p in powerup_hits:
        if p.type == 'heal':
            player.health += player.max_health // 5
            if player.health > player.max_health:
                player.health = player.max_health
        elif p.type == 'recoil':
            player.recoil = 5
            player.recoil_effect_active = True
            player.recoil_timer = pygame.time.get_ticks()

    screen.blit(pozadi, (0, 0))
    Vsechny_sprites_group.draw(screen)
    player.draw_health_bar(screen)

    for zombie in enemy_group:
        zombie.draw_health_bar(screen)

    
    kills_text = font.render(f"kills: {kills}", True, (255, 255, 255))
    screen.blit(kills_text, (10, 40))

    if player.health <= 0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            text = font.render("MEGA L", True, (255, 0, 0))
            screen.blit(text, (sirka // 2 - text.get_width() // 2, vyska // 2 - text.get_height() // 2))
            pygame.display.update()
            
            running = False
            
    pygame.display.update()

pygame.quit()
exit()