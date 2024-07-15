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

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

GAME_WIDTH, GAME_HEIGHT = 1920,1080

MapSize = (800,600)

WOOD_BROWN = (97, 54, 19)

Turet_Type = 1
do_cheats = False
do_particles = True



# Initialize Pygame









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




# Game loop
def main():
    
    engine.init((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    
    
    UI = engine.UI()
    scroll_size = (200,SCREEN_HEIGHT)
    scroll_area = UI.new_scroll_area(position=((SCREEN_WIDTH - scroll_size[0]), 0), size=scroll_size, backround_color=WOOD_BROWN ,texture=engine.Image().LoadImage("menu_backround"))
    global DEBUG
    # Screen dimensions
    pygame.init()
    SCREEN = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption("Your Average Tower Defence Game")

    Player_Class = User()
    
    logoImage = engine.Image().LoadIcon("logo.png")
    
    

    MESSAGE = None

    GUIdebug = engine.GUIdebug(SCREEN)
    
    
    
    def set_sellect_turret(id):
        global Turet_Type
        Turet_Type = id
        
    
    
    
    scroll_area.new_button("Turret", lambda: set_sellect_turret(1), texture=engine.Image().LoadImage("wood_button"))
    scroll_area.new_button("Missle", lambda: set_sellect_turret(2), texture=engine.Image().LoadImage("wood_button"))
    scroll_area.new_button("Button 3", lambda: set_sellect_turret(3), texture=engine.Image().LoadImage("wood_button"))
    scroll_area.new_button("Button 4", lambda: set_sellect_turret(4), texture=engine.Image().LoadImage("wood_button"))
    scroll_area.new_button("Button 5", lambda: set_sellect_turret(5), texture=engine.Image().LoadImage("wood_button"))
    
    





    MapImage = engine.Image().LoadImage("map")
    
    
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

    dt = 0
    
    heartImage = engine.Image().LoadImage("heart")
    skullImage = engine.Image().LoadImage("skull")
    coinImage = engine.Image().LoadImage("coin")
    
    heartImage = pygame.transform.smoothscale(heartImage, (30,30))
    skullImage = pygame.transform.smoothscale(skullImage, (30,30))
    coinImage = pygame.transform.smoothscale(coinImage, (40,40))
    
    down = False
    DrawTerminal = False
    
    musicClass = engine.Sound()
    
    def command_handler(command):
        global do_cheats, do_particles
        if command.startswith("exit"):
            sys.exit()
        elif command.startswith("echo"):
            command = command.split(" ")
            Terminal.print_text(" ".join(command[1:]))
        elif command.startswith("cheats_toggle"):
            do_cheats = not do_cheats
        elif command.startswith("money_give"):
            if not do_cheats:
                Terminal.print_text("Cheats not enabled, do cheats_toggle to enable cheats")
                
                return
            command = command.split(" ")
            Player_Class.money += int(command[1])
            
        elif command.startswith("setting"):
            command = command.split(" ")
            if command[1] == "music":
                if command[2] == "on":
                    Terminal.print_text("Turned music on")
                    
                    musicClass.set_music_status(True)
                elif command[2] == "off":
                    Terminal.print_text("Turned music off")
                    
                    musicClass.set_music_status(False)
            elif command[1] == "do_particles":
                try:
                    if command[2].lower() in ["on", "true", "1"]:
                        do_particles = True
                    elif command[2].lower() in ["off", "false", "0"]:
                        do_particles = False
                    print(command,do_particles)
                    
                except:
                    Terminal.print_text("Invalid boolean value for setting do_particles")
        
    
            
    Terminal = engine.Terminal((200,200), input=True, callback=command_handler)
    
    
    tourch = game.TourchItem((400,400))  
    
    

    while running:
        
        # Check if it's time to spawn an enemy
        if ticks >= (SPAWN_SPEED * (dt + 1)):
            ticks = 0
            enemies.append(game.Enemy(find_path(TILE_MAP, TILE_SIZE), random.randrange(1,13)))
            
        

        SCREEN.fill(COLOR.WHITE)
        SCREEN.blit(MapImage, (0,0))
        if DEBUG:
            for tile in tiles:
                tile.draw(SCREEN)

        for tower in towers:
            tower.draw(SCREEN)
            tower.update()
            if DEBUG:
                mouse_pos = engine.get_mouse_pos()
                GUIdebug.drawDebugText(str(tower.kills), Text=f"Kills {tower.id}")
                if engine.Check().point_inside_rect( mouse_pos, tower.rect ):
                            GUIdebug.drawDebugText(str(tower.level), Text=f"level {str(tower.id)}")
            # Attack logic
            if len(enemies) > 0:
                bullet = tower.attack(enemies, dt)
                if bullet:
                    bullets.append(bullet)

        for bullet in bullets[:]:
            bullet.move(dt)
            bullet.draw(SCREEN)
            
            if bullet.target.Targeted:
                if bullet.target.health >= bullet.damage+1:
                    bullet.target.Targeted = False
                    
            
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
                Player_Class.health -= enemy.health
                
                enemies.remove(enemy)
                if do_particles:
                    for _ in range(20):  # Example number of particles
                        velocity = (random.uniform(-6, 6), random.uniform(-6, 6))
                        size = random.uniform(5, 15)
                        color = COLOR.RED
                        particles.append(engine.Particle(enemy.position, velocity, size, color))
                engine.Sound().PlayFX("enemy_complete")
                
                break
                
                
            enemy.move(dt)
            
            enemy.draw(SCREEN)
            if enemy.x > SCREEN_WIDTH:
                enemies.remove(enemy)
            if enemy.health <= 0:
                Player_Class.money += enemy.max_health
            if enemy.health <= 0:
                # Create explosion particles
                if do_particles:
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
            UI.handle_event(event)
            Terminal.handle_events(event)
            
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    Terminal.active = True
                    DrawTerminal = not DrawTerminal
                if event.key == pygame.K_F3:
                    DEBUG = not DEBUG
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if down:
                        continue
                    down = True
                    mouse_x, mouse_y = engine.get_mouse_pos()
                    
                    mouse_pos = engine.get_mouse_pos()
                    canPlace = True
                    if DrawTerminal:
                        if engine.Check().point_inside_rect( mouse_pos, Terminal.rect ):
                            continue
                    
                    for tower in towers:
                        if engine.Check().point_inside_rect( mouse_pos, tower.rect ):
                            
                            canPlace = False
                            if Player_Class.money >= tower.get_next_level_price() and tower.can_upgrade():
                                tower.upgrade(Player_Class)
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
                    if Turet_Type == 1:
                        towers.append(game.Tower(mouse_x, mouse_y, len(towers)))
                    elif Turet_Type == 2:        
                        towers.append(game.Missile(mouse_x, mouse_y, len(towers), do_particles=do_particles))
                            
                            #towers.append(game.Cannon(mouse_x, mouse_y, len(towers)))
                            
                            #towers.append(game.FlameThrower(mouse_x, mouse_y, len(towers)))
                            
                            #towers.append(game.Laser(mouse_x, mouse_y, len(towers)))
                            
                    #towers.append(game.Tower(mouse_x, mouse_y, len(towers)))
                    engine.Sound().PlayFX("turret_place")
                else:
                    down = False
            
                    
                    
                
        else:
            down = False
            
        
        if do_particles:
            for particle in particles[:]:
                particle.update()
                particle.draw(SCREEN)
                if not particle.is_alive():
                    particles.remove(particle)
                    
        try:
            MESSAGE.update()
        except:
            pass
        #print(Turet_Type)
        
        
        if DEBUG:
            GUIdebug.NewFrame()
            GUIdebug.drawDebugText("DEBUG MENU", False)
            GUIdebug.drawDebugText(f"{int(clock.get_fps())}", Text="FPS")

            GUIdebug.drawDebugText(f"{len(enemies)}", Text="Enemies")
            GUIdebug.drawDebugText(str(Player_Class.money), Text="Money")
            GUIdebug.drawDebugText(str(Player_Class.kills), Text="Kills")
            
            for tower in towers[:]:
                engine.draw_text_center(SCREEN, f"lvl:{tower.level}", (tower.position[0], tower.position[1]+30), 25)
                
                engine.draw_text_center(SCREEN, f"dmg:{tower.damage}", (tower.position[0], tower.position[1]+45), 25)
                
                
            
        else:
            SCREEN.blit(coinImage, (10,10))
            engine.draw_text_left(SCREEN, "     " + str(Player_Class.money), (10,15), 50)
            SCREEN.blit(skullImage, (15,60))
            engine.draw_text_left(SCREEN, "     " + str(Player_Class.kills), (10,65), 40)
            SCREEN.blit(heartImage, (10,95))
            engine.draw_text_left(SCREEN, "     " + str(Player_Class.health), (10,100), 40)


        if do_particles:
            tourch.draw(SCREEN, dt)
        
        for doller in appendedMoney:
            Player_Class.money += doller
            appendedMoney.pop(0)
            
        UI.draw(SCREEN)
        SCREEN.blit(logoImage, (SCREEN_WIDTH-50,SCREEN_HEIGHT-50))
        
        if DrawTerminal:
            
            Terminal.draw(SCREEN,dt)
        else:
            Terminal.active - False
            
            
            
            
            
            
            
        engine.tick(SCREEN, dt)
        
        
        
        # DONT PUT ANYTHING BELOW
        scaled_surface = pygame.transform.scale(SCREEN, (GAME_WIDTH, GAME_HEIGHT))
        
        

        # Blit the scaled surface to the display surface
        game_window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        ticks += 1
        
        
        
        
        musicClass.PlayMusicRandom(0.1)
        dt = clock.tick() / 1000.0

    pygame.quit()

def is_on_path(x, y):
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    
    if x >= MapSize[0]:
        return True
    
    # Check if the calculated indices are within bounds
    if 0 <= tile_y < len(TILE_MAP) and 0 <= tile_x < len(TILE_MAP[0]):
        return TILE_MAP[tile_y][tile_x] == 1
    
    # Default to False if coordinates are out of bounds
    return False





def draw_button(screen, color, rect, text, font, text_color):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    
def new_random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
def lerp(a, b, t):
    return a + (b - a) * t
def run():
    pygame.init()
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    BUTTON_WIDTH, BUTTON_HEIGHT = 200, 80
    BUTTON_COLOR = (100, 200, 100)
    BUTTON_HOVER_COLOR = (150, 250, 150)
    TEXT_COLOR = (255, 255, 255)
    FONT_SIZE = 36
    FPS = 60

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Your Average Loading Menu")

    # Font setup
    font = pygame.font.Font(None, FONT_SIZE)

    # Animation variables
    tick = 0
    particles = []
    button_color = BUTTON_COLOR

    # Load and animate the logo/icon
    logo_image = pygame.image.load('./assets/icon/logo.png')
    logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, (SCREEN_HEIGHT - BUTTON_HEIGHT) // 2, BUTTON_WIDTH, BUTTON_HEIGHT)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    main()  # Replace with your main function or game loop
                    return

        # Update particles
        tick += 1
        screen.fill((40,40, 40))

        # Draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if not particle.is_alive():
                particles.remove(particle)

        # Generate new particles periodically
        if tick % 2 == 0:
            for _ in range(2):  # Example number of particles
                velocity = (random.uniform(-2, 2), random.uniform(-2, 2))
                size = random.uniform(10, 20)
                color = new_random_color()
                particles.append(engine.Particle((random.randint(0, SCREEN_WIDTH), (random.randint(0, SCREEN_HEIGHT))), velocity, size, color))

        # Update button hover effect
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            button_color = BUTTON_HOVER_COLOR
        else:
            button_color = BUTTON_COLOR

        # Draw button
        draw_button(screen, button_color, button_rect, "Play", font, TEXT_COLOR)

        # Animate logo/icon scaling and movement
        

        # Draw logo/icon
        screen.blit(logo_image, (10,10))

        # Draw title
        title_surf = font.render("Loading Menu", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surf, title_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run()