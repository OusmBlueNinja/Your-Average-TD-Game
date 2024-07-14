import pygame
import sys
import math
import time
import random 


import lib.classes as game
import lib.engine as engine
from lib.engine import COLOR
from lib.config import *
from lib.user import User

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600




# Initialize Pygame
pygame.init()
engine.__init__((SCREEN_WIDTH,SCREEN_HEIGHT))



# Screen dimensions

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Your Average Tower Defence Game")

Player_Class = User()




def find_path(tile_map, tile_size) -> list[tuple[int, int]]:
    path = []
    
    # Find the starting point (assuming it's marked by '2') and the ending point ('3')
    start_x = None
    start_y = None
    end_x = None
    end_y = None
    
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == 2:
                start_x = x
                start_y = y
            elif tile == 3:
                end_x = x
                end_y = y
    
    if start_x is None or start_y is None:
        raise ValueError("Starting point '2' not found in TILE_MAP.")
    if end_x is None or end_y is None:
        raise ValueError("Ending point '3' not found in TILE_MAP.")
    
    # Determine the initial direction based on adjacent '1' tiles
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, down, left, up
    for dx, dy in directions:
        if 0 <= start_x + dx < len(tile_map[0]) and 0 <= start_y + dy < len(tile_map):
            if tile_map[start_y + dy][start_x + dx] == 1:
                current_x = start_x + dx
                current_y = start_y + dy
                direction = (dx, dy)
                break
    
    # Traverse the path according to the '1' tiles, avoiding the previous direction
    while (current_x, current_y) != (end_x, end_y):
        path.append((current_x * tile_size, current_y * tile_size + 20))  # Adjusted for your requirement
        
        # Determine possible directions
        possible_directions = []
        for dx, dy in directions:
            if (dx, dy) != (-direction[0], -direction[1]):  # Avoid going back where it came from
                new_x = current_x + dx
                new_y = current_y + dy
                if 0 <= new_x < len(tile_map[0]) and 0 <= new_y < len(tile_map):
                    if tile_map[new_y][new_x] == 1:
                        possible_directions.append((dx, dy))
        
        # Choose the next direction randomly from possible directions
        if possible_directions:
            direction = possible_directions[random.randint(0, len(possible_directions) - 1)]
            current_x += direction[0]
            current_y += direction[1]
        else:
            break  # No valid path found
    
    # Add the end point ('3') to the path
    path.append((end_x * tile_size, end_y * tile_size + 20))
    
    return path



MESSAGE = None

GUIdebug = engine.GUIdebug(SCREEN)





MapImage = engine.Image().LoadImage("map")


# Game loop
def main():
    global DEBUG
    clock = pygame.time.Clock()
    running = True
    tiles = [game.Tile(x, y, TILE_MAP[y][x]) for y in range(len(TILE_MAP)) for x in range(len(TILE_MAP[0]))]
    towers = []
    enemies = []  # No initial enemies
    bullets = []  # Initialize bullets as an empty list
    ticks = 0
    ticks = 0
    particles = []
    appendedMoney = []
    
    heartImage = engine.Image().LoadImage("heart")
    skullImage = engine.Image().LoadImage("skull")
    coinImage = engine.Image().LoadImage("coin")
    
    heartImage = pygame.transform.smoothscale(heartImage, (30,30))
    skullImage = pygame.transform.smoothscale(skullImage, (30,30))
    coinImage = pygame.transform.smoothscale(coinImage, (40,40))
    
    down = False
    
    musicClass = engine.Sound()
    

    while running:
        
        # Check if it's time to spawn an enemy
        if ticks >= SPAWN_SPEED:
            ticks = 0
            enemies.append(game.Enemy(find_path(TILE_MAP, TILE_SIZE), random.randrange(1,13)))
            
        

        SCREEN.fill(COLOR.WHITE)
        SCREEN.blit(MapImage, (0,0))
        if DEBUG:
            for tile in tiles:
                tile.draw(SCREEN)

        for tower in towers:
            tower.draw(SCREEN)
            if DEBUG:
                mouse_pos = engine.get_mouse_pos()
                GUIdebug.drawDebugText(str(tower.kills), Text=f"Kills {tower.id}")
                if engine.Check().point_inside_rect( mouse_pos, tower.rect ):
                            GUIdebug.drawDebugText(str(tower.level), Text=f"level {str(tower.id)}")
            # Attack logic
            if len(enemies) > 0:
                bullet = tower.attack(enemies)
                if bullet:
                    bullets.append(bullet)

        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(SCREEN)
            if math.sqrt((bullet.target.position[0] - bullet.x) ** 2 + (bullet.target.position[1] - bullet.y) ** 2) < 10:
                bullet.target.health -= bullet.damage
                if bullet.target.health <= 0:
                    for tower in towers:
                        if tower.position == bullet.position:  # Example check for the tower
                            Player_Class.kills += 1
                            tower.kills += 1
                            break
                bullets.remove(bullet)
            
            

        for enemy in enemies:
            
            if enemy.done:
                Player_Class.health -= enemy.max_health
                
                enemies.remove(enemy)
                for _ in range(20):  # Example number of particles
                    velocity = (random.uniform(-6, 6), random.uniform(-6, 6))
                    size = random.uniform(5, 15)
                    color = COLOR.RED
                    particles.append(engine.Particle(enemy.position, velocity, size, color))
                engine.Sound().PlayFX("enemy_complete")
                
                break
                
                
            enemy.move()
            enemy.draw(SCREEN)
            if enemy.x > SCREEN_WIDTH:
                enemies.remove(enemy)
            if enemy.health <= 0:
                Player_Class.money += enemy.max_health
            if enemy.health <= 0:
                # Create explosion particles
                for _ in range(20):  # Example number of particles
                    velocity = (random.uniform(-3, 3), random.uniform(-3, 3))
                    size = random.uniform(5, 10)
                    color = COLOR.BLACK
                    particles.append(engine.Particle(enemy.position, velocity, size, color))
                # Remove enemy
                for _ in range(enemy.max_health):
                    appendedMoney.append(1) 
                engine.Sound().PlayFX("enemy_explode")
                enemies.remove(enemy)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if down:
                        continue
                    down = True
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    mouse_pos = engine.get_mouse_pos()
                    canPlace = True
                    for tower in towers:
                        if engine.Check().point_inside_rect( mouse_pos, tower.rect ):
                            
                            canPlace = False
                            if Player_Class.money >= tower.get_next_level_price() and tower.can_upgrade():
                                tower.upgrade(Player_Class.money)
                                break
                    
                    if is_on_path(mouse_x, mouse_y):
                        continue
                    if Player_Class.money <= 100: # Tower Cost
                        MESSAGE = engine.FlashMessage(SCREEN, "Not Enough Money")
                        MESSAGE.start()
                        
                        continue
                    if not canPlace:
                        continue
                    
                    Player_Class.money -= 100
                    towers.append(game.Tower(mouse_x, mouse_y, len(towers)))
                    engine.Sound().PlayFX("turret_place")
                else:
                    down = False
            
                    
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    DEBUG = not DEBUG
        else:
            down = False
        
        for particle in particles[:]:
            particle.update()
            particle.draw(SCREEN)
            if not particle.is_alive():
                particles.remove(particle)
                    
        try:
            MESSAGE.update()
        except:
            pass
        if DEBUG:
            GUIdebug.NewFrame()
            GUIdebug.drawDebugText("DEBUG MENU", False)
            GUIdebug.drawDebugText(f"{len(enemies)}", Text="Enemies")
            GUIdebug.drawDebugText(str(Player_Class.money), Text="Money")
            GUIdebug.drawDebugText(str(Player_Class.kills), Text="Kills")
            
        else:
            SCREEN.blit(coinImage, (10,10))
            engine.draw_text_left(SCREEN, "     " + str(Player_Class.money), (10,15), 50)
            SCREEN.blit(skullImage, (15,60))
            engine.draw_text_left(SCREEN, "     " + str(Player_Class.kills), (10,65), 40)
            SCREEN.blit(heartImage, (10,95))
            engine.draw_text_left(SCREEN, "     " + str(Player_Class.health), (10,100), 40)

        
        for doller in appendedMoney:
            Player_Class.money += doller
            appendedMoney.pop(0)
        
        pygame.display.update()
        ticks += 1
        
        musicClass.PlayMusicRandom(0.1)
        clock.tick(FPS)

    pygame.quit()

def is_on_path(x, y):
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    
    # Check if the calculated indices are within bounds
    if 0 <= tile_y < len(TILE_MAP) and 0 <= tile_x < len(TILE_MAP[0]):
        return TILE_MAP[tile_y][tile_x] == 1
    
    # Default to False if coordinates are out of bounds
    return False


if __name__ == "__main__":
    main()
