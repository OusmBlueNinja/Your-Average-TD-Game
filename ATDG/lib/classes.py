import pygame
from lib.engine import COLOR
import lib.engine as engine
import math, random
from lib.config import TILE_SIZE




class Tile:
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.tile_type = tile_type

    def draw(self, screen):
        color = COLOR.GREEN
        if self.tile_type != 0:
            pygame.draw.rect(screen, color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE/4, TILE_SIZE/4))

class Tower:
    def __init__(self, x, y, id):
        self.id = id
        self.x = x
        self.y = y
        self.position = (x,y)
        self.range = 200
        self.damage = 20
        self.level = 1
        self.attack_speed = 0.5  # Lower is slower
        self.cooldown = 0  # Cooldown counter
        self.max_cooldown = 30  # Maximum cooldown frames
        self._tower_size = 20
        
        self.speed = 10
        
        self.max_level = 0
        
        
        # Assets
        self.tripod_image = engine.Image().LoadImage("turret_base")
        self.turret_image = engine.Image().LoadImage("turret_top_0")
        
        
        self.image = self.turret_image
        self.rect = self.image.get_rect(center=self.position)
        self.original_image = self.image
        self.position = self.position
        self.angle = 0
        
        
        
        
        
        self.kills = 0
        
    def update(self):
        return

    def draw(self, screen):
        # Calculate the center position based on the image dimensions
        image_rect = self.tripod_image.get_rect()
        center_x = self.x - image_rect.width // 2
        center_y = self.y - image_rect.height // 2

        # Blit the image to the screen centered at (center_x, center_y)
        screen.blit(self.tripod_image, (center_x, center_y))
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Call additional drawing methods or effects here
        self.onHover(screen)


    def upgrade(self, player):
        
        if self.level > 2:
            return
        self.damage += 10
        self.range += 20
        self.attack_speed += 0.5  # Increase attack speed on upgrade
        
        self.speed += 5
        
        
        try:
            self.turret_image = engine.Image().LoadImage(f"turret_top_{self.level}")
            self.image = engine.Image().LoadImage(f"turret_top_{self.level}")
            self.original_image = self.image.copy()
        except:
            if self.max_level == 0:
                self.max_level = self.level - 1
            self.image = engine.Image().LoadImage(f"turret_top_{self.max_level}")
            self.original_image = self.image.copy()
        player.money -= self.get_next_level_price()
        self.level += 1
        engine.Sound().PlayFX("turret_upgrade")
            
    def get_next_level_price(self):
        return 110 * self.level * (self.level + 1)  # Formula for calculating upgrade cost
    
    def can_upgrade(self):
        return False if self.level >= 5 else True
        
    def rotate_towards_target(self, target_position):
        # Calculate angle to target
        direction = pygame.math.Vector2(target_position) - self.position
        self.angle = -math.degrees(math.atan2(direction.y, direction.x)) - 90

        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def attack(self, enemies, dt):
        if self.cooldown > 0:
            self.cooldown -= self.attack_speed * ( dt +1 )
            return None

        for enemy in enemies:
            if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 < self.range ** 2:
                self.cooldown = self.max_cooldown  # Reset cooldown
                self.rotate_towards_target((enemy.x, enemy.y))
                engine.Sound().PlayFX(f"turret_shoot_{self.level}")
                return Bullet(self.x, self.y, enemy, self.damage, speed=self.speed)

        return None
    
    def onHover(self,screen):
        range_rect = pygame.Rect(self.x - self._tower_size, self.y - self._tower_size,
                             self._tower_size * 2, self._tower_size * 2)

        mouse_pos = engine.get_mouse_pos()
        if engine.Check().point_inside_rect( mouse_pos, range_rect ):
            pygame.draw.circle(screen, COLOR.BLACK, (self.x, self.y), self.range, 1)  # Draw in red if mouse inside
            
            engine.draw_text_center(screen,f"Cost: {self.get_next_level_price()}" , mouse_pos, 15)
            
class Missile:
    def __init__(self, x, y, id, do_particles=True):
        self.id = id
        self.x = x
        self.y = y
        self.position = (x, y)
        self.range = 300
        self.damage = 80
        self.level = 1
        self.attack_speed = 0.1  # Lower is slower
        self.cooldown = 0  # Cooldown counter
        self.max_cooldown = 30  # Maximum cooldown frames
        self._tower_size = 20

        self.do_particles = do_particles
        
        self.speed = 4

        self.max_level = 0

        # Assets
        self.frames = ["missle_0","missle_1", "missle_2", "missle_3", "missle_4", "missle_5", "missle_open"]
        self.animation = engine.Image().LoadAnimation(self.frames)

        self.image = self.animation[0]  # Initial image from animation frames
        self.rect = self.image.get_rect(center=self.position)
        self.original_image = self.image
        self.position = self.position
        self.angle = 0

        self.kills = 0
        self.shooting_animation_index = 0
        self.is_shooting = False

    def draw(self, screen):
        # Calculate the center position based on the image dimensions
        image_rect = self.rect
        center_x = self.x - image_rect.width // 2
        center_y = self.y - image_rect.height // 2

        # Blit the image to the screen centered at (center_x, center_y)
        screen.blit(self.image, (center_x, center_y))

        # Call additional drawing methods or effects here
        self.onHover(screen)

    def update_shooting_animation(self):
        if self.is_shooting:
            
            if self.shooting_animation_index >= len(self.frames)-1:
                self.is_shooting = False
            else:
                self.shooting_animation_index += 1
            
        else:
            if self.shooting_animation_index >= 1:
                self.shooting_animation_index -= 1
        self.image = self.animation[self.shooting_animation_index]
            

    def upgrade(self, player):
        if self.level > 2:
            return
        self.damage += 100
        self.range += 200
        self.attack_speed += 0.1  # Increase attack speed on upgrade
        
        self.speed = 5

        
        player.money -= self.get_next_level_price()
        self.level += 1
        engine.Sound().PlayFX("missle_upgrade")

    def get_next_level_price(self):
        return 600 * self.level * (self.level + 1)  # Formula for calculating upgrade cost

    def can_upgrade(self):
        return False if self.level >= 5 else True


    def attack(self, enemies, dt):
        if self.cooldown > 0:
            self.cooldown -= self.attack_speed * ( dt +1 )
            return None

        for enemy in enemies:
            if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 < self.range ** 2 and not enemy.Targeted:
                self.cooldown = self.max_cooldown  # Reset cooldown
                engine.Sound().PlayFX(f"missle_shoot")
                self.is_shooting = True
                self.update_shooting_animation()
                enemy.Targeted = True
                return Bullet(self.x, self.y, enemy, self.damage, trail=self.do_particles, speed=self.speed)

        return None

    def onHover(self, screen):
        range_rect = pygame.Rect(self.x - self._tower_size, self.y - self._tower_size,
                                 self._tower_size * 2, self._tower_size * 2)

        mouse_pos = engine.get_mouse_pos()
        if engine.Check().point_inside_rect(mouse_pos, range_rect):
            pygame.draw.circle(screen, COLOR.BLACK, (self.x, self.y), self.range, 1)  # Draw in black if mouse inside

            engine.draw_text_center(screen, f"Cost: {self.get_next_level_price()}", mouse_pos, 15)

    def update(self):
        self.update_shooting_animation()

    
            
    
class TourchItem:
    def __init__(self, position):
        self.position = position
        self.particles = []
    def draw(self, screen, deltatime):
        if 1:
            pygame.draw.rect(screen, COLOR.BROWN, (self.position[0], self.position[1], 5,15))

            for particle in self.particles[:]:
                particle.update()
                particle.draw(screen)
                if not particle.is_alive():
                    self.particles.remove(particle)
            velocity = (random.uniform(-0.4,0.4),-1-random.uniform(-0.5,0.5))
            size = random.uniform(3,5)
            color = random.choice([COLOR.RED, COLOR.ORANGE, COLOR.YELLOW])
            self.particles.append(engine.Particle((self.position[0]+3,self.position[1]), velocity, size, color))
        

class Bullet:
    def __init__(self, x, y, target, damage, trail=False, speed=5):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.target = target
        self.damage = damage
        self.speed = speed
        self.trail = trail
        self.particles = []

    def move(self, dt):
        target_x, target_y = self.target.x, self.target.y
        dx, dy = target_x - self.x, target_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist != 0:
            self.x += (self.speed * (dt+1)) * dx / dist
            self.y += (self.speed* (dt+1)) * dy / dist

    def draw(self, screen):
        if self.trail:
            for particle in self.particles[:]:
                particle.update()
                particle.draw(screen)
                if not particle.is_alive():
                    self.particles.remove(particle)
            velocity = (random.random(),random.random())
            size = 5
            color = COLOR.RED
            self.particles.append(engine.Particle((self.x,self.y), velocity, size, color))
        pygame.draw.circle(screen, COLOR.BLACK, (int(self.x), int(self.y)), 5)



                    
                    
class Enemy:
    def __init__(self, path, level):
        
        self.done = False
        
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[self.path_index]
        self.position = (0,0)
        self.ENEMY_PROPERTIES = {
            1: {"health": 40, "speed": 1.8, "color": COLOR.PINK},
            2: {"health": 20, "speed": 0.8, "color": COLOR.MAGENTA},
            3: {"health": 30, "speed": 0.6, "color": COLOR.ORANGE},
            4: {"health": 40, "speed": 1.5, "color": COLOR.BLUE},
            5: {"health": 50, "speed": 1.4, "color": COLOR.RED},
            6: {"health": 60, "speed": 0.3, "color": COLOR.CYAN},
            7: {"health": 70, "speed": 0.8, "color": COLOR.MAGENTA},
            8: {"health": 80, "speed": 0.6, "color": COLOR.ORANGE},
            9: {"health": 90, "speed": 0.5, "color": COLOR.BLUE},
            10: {"health": 100, "speed": 0.8, "color": COLOR.RED},
            11: {"health": 150, "speed": 0.3, "color": COLOR.RED},
            12: {"health": 200, "speed": 0.2, "color": COLOR.RED},
            13: {"health": 250, "speed": 0.1, "color": COLOR.BLUE},
        }
        
        self.sizex, self.sizey = 20,20
        
        # Fetch properties based on level
        properties = self.ENEMY_PROPERTIES.get(level, self.ENEMY_PROPERTIES[1])
        self.health = properties["health"]
        self.max_health = properties["health"]
        self.speed = properties["speed"]
        self.color = properties["color"]
        
        self.Targeted = False

    def move(self, dt):
        if self.path_index < len(self.path) - 1:
            
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist != 0:
                self.x += (min(self.speed, dist)* (dt+1)) * dx / dist
                self.y += (min(self.speed, dist) * (dt+1)) * dy / dist

            if dist < self.speed:
                self.path_index += 1
                if self.path_index < len(self.path):
                    self.x, self.y = self.path[self.path_index]
        else:
            self.done = True

    def draw(self, screen):
        self.position = (self.x, self.y)
        pygame.draw.rect(screen, COLOR.BLACK, (int(self.x-1), int(self.y-1), self.sizex+2, self.sizey+2))
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.sizex, self.sizey))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        if self.health == self.max_health:
            return
        health_ratio = self.health / self.max_health
        bar_width = int(self.sizex * health_ratio)
        pygame.draw.rect(screen, COLOR.BLACK, (int(self.x-1), int(self.y-1) - 10, self.sizex+2, 7))
        pygame.draw.rect(screen, COLOR.RED, (int(self.x), int(self.y) - 10, self.sizex, 5))
        pygame.draw.rect(screen, COLOR.GREEN, (int(self.x), int(self.y) - 10, bar_width, 5))
        
    
            

