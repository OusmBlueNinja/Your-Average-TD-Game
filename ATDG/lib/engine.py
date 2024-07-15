import pygame, time, math, datetime, os, sys, random

pygame.font.init()

version = "1.6.8"

_delta_time = 0


class COLOR:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    BROWN = (165, 42, 42)
    GRAY = (128, 128, 128)
    PINK = (255, 192, 203)
    LIGHT_BLUE = (173, 216, 230)
    DARK_GREEN = (0, 100, 0)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    CLEAR = (0,0,0,0)
    
COLOR = COLOR()

class Logger:
    
    def __init__(self):
        
        os.makedirs("./logs/", exist_ok=True)
        with open("./logs/latest.log", "w") as f:
            f.write("")
    def log(self,message):
        with open("./logs/latest.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] [INFO] {message}\n")
    def debug(self,message):
        with open("./logs/latest.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] [DEBG] {message}\n")
    def warn(self,message):
        with open("./logs/latest.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] [WARN] {message}\n")
    def error(self,message):
        with open("./logs/latest.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] [EROR] {message}\n")
            
            
logger = Logger()




def init(screen_size: tuple):
    global _SCREEN_SIZE, _SCREEN_HEIGHT, _SCREEN_WIDTH, _CURSOR_ICON
    _SCREEN_SIZE = screen_size
    _SCREEN_HEIGHT, _SCREEN_WIDTH = _SCREEN_SIZE
    
    
    pygame.init()
    
    pygame.mouse.set_visible(False)
    
    
    
    print(f"OBEngine {version}")
    print(f"https://github.com/OusmBlueNinja/OBEngine")
    
    logger.log(f"Initializing screen size [ {screen_size} ]")
    
    logger.log(f"Creating Engine Folder")
    
    os.makedirs("./assets/images", exist_ok=True)
    os.makedirs("./assets/music", exist_ok=True)
    os.makedirs("./assets/fx", exist_ok=True)
    os.makedirs("./assets/icon", exist_ok=True)
    
    icon_folder = "./assets/icon"
    icons = [f for f in os.listdir(icon_folder) if f.endswith('.png')]
    
    
    if not icons or "logo.png" not in icons:
        print(icons)
        logger.warn("No Icon Found")
    else:
        pygame.display.set_icon(Image().LoadIcon(icons[icons.index("logo.png")]))
        
        
    if not icons or "cursor.png" not in icons:
        print(icons)
        logger.warn("No Cursor Found")
        _CURSOR_ICON = None
    else:
        _CURSOR_ICON = Image().LoadIcon(icons[icons.index("cursor.png")])
        

    

def tick(screen, delta_time):
    global _delta_time
    _delta_time = delta_time
    """Called Every Game Tick"""
    # Draw Cursor
    if _CURSOR_ICON:
        screen.blit(_CURSOR_ICON, pygame.mouse.get_pos())
    else:
        
        pygame.draw.line(screen, COLOR.WHITE, (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1]), (pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1]), 2)
        pygame.draw.line(screen, COLOR.WHITE, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 10), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 10), 2)
        
    








class FlashMessage:
    def __init__(self, screen, message, duration=2.5):
        self.font = pygame.font.SysFont("Contage", 36)
        self.screen = screen
        self.message = message
        self.duration = duration
        self.start_time = None
        self.active = False
        self.text_surface = self.font.render(self.message, True, COLOR.BLACK)
        self.text_rect = self.text_surface.get_rect(center=(_SCREEN_WIDTH / 2, _SCREEN_HEIGHT / 2))

    def start(self) -> None:
        self.start_time = time.time()
        self.active = True

    def update(self) -> None:
        if self.active and time.time() - self.start_time < self.duration:
            self.screen.blit(self.text_surface, self.text_rect)
        elif self.active:
            self.active = False
        
def draw_text_center(screen, message: str, position: tuple, size:int) -> None:
    font_Calibri = pygame.font.SysFont("Contage", size)
    text_surface = font_Calibri.render(message, True, COLOR.BLACK)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def draw_text_left(screen, message: str, position: tuple, size:int) -> None:
    font_Calibri = pygame.font.SysFont("Contage", size)
    text_surface = font_Calibri.render(message, True, COLOR.BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = position
    screen.blit(text_surface, text_rect)
    
    
class Check:
    def __init__(self):
        pass
    def point_inside_rect(self, point, rect):
        x, y = point
        return rect.collidepoint(x, y)
    



def middle_point(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    mx = ((x1 + x2) / 1.9)
    my = ((y1 + y2) / 1.9)
    return (mx, my)

    
def get_mouse_pos() -> tuple[int, int] :

    # Get the mouse position
    return pygame.mouse.get_pos()

class GUIdebug:
    def __init__(self, screen):
        self.screen = screen
        self.id = 0
    def NewFrame(self):
        self.id = 0
    def drawDebugText(self, text: any, Format=True, Text="None"):
        
            
        if not Format:
            font = pygame.font.Font("freesansbold.ttf", 20)
            size = (3, 3)
            text = str(text)
        else:
            self.id += 1
            id = self.id
            _id = "P"+str(id)
            #print(Text)
            if Text!="None":
               _id = Text
            
            font = pygame.font.Font("freesansbold.ttf", 15)
            size = (5, ((id*17)+5))
            text = f"({_id}): " + str(text)

        text = font.render(text, 1, (80,80,80))
        self.screen.blit(text, size)
    
    
class Particle:
    def __init__(self, position, velocity, size, color):
        self.position = list(position)  # Position as [x, y]
        self.velocity = list(velocity)  # Velocity as [vx, vy]
        self.size = size  # Particle size
        self.color = color  # Particle color
        self.lifetime = 100  # Example lifetime (adjust as needed)
        self.age = 0  # Initial age of the particle

    def update(self):
        # Update position based on velocity
        self.position[0] += self.velocity[0] * (_delta_time+1)
        self.position[1] += self.velocity[1] * (_delta_time+1)

        # Update age
        self.age += 1 * _delta_time
        self.size -= 0.01

        # Gradually decrease size as particle ages
        if self.age <= self.lifetime // 2:
            self.size -= 0.1

    def draw(self, screen):
        # Draw the particle as a simple circle
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), int(self.size))

    def is_alive(self):
        # Check if the particle is still alive based on its age and lifetime
        return self.age < self.lifetime
    
class Math:
    def __init__(self):
        super().__init__()
        pass
    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t
    
    
class Image:
    def LoadImage(self, ImageName:str) -> pygame.Surface:
        try:
            logger.log(f"Loading Image: %s" % ImageName)
            return pygame.image.load(f"./assets/images/{ImageName}.png")
        except pygame.error as message:
            logger.error(("Unable to load image:", ImageName))
            logger.error(("Error:", message))
            return None
        
    def LoadIcon(self, IconName:str) -> pygame.Surface:
        try:
            logger.log(f"Loading Icon: %s" % IconName)
            return pygame.image.load(f"./assets/icon/{IconName}")
        except pygame.error as message:
            logger.error(("Unable to load icon:", IconName))
            logger.error(("Error:", message))
            return None
        
    def LoadAnimation(self, ImageNames: list[str]) -> list[pygame.Surface]:
        """Load an animation from a list of image files"""
        images = []
        
        logger.log(f"Loading Animation Frames: %s" % ImageNames)
        for ImageName in ImageNames:
            try:
                images.append(pygame.image.load(f"./assets/images/{ImageName}.png"))
            except pygame.error as message:
                logger.error(("Unable to load icon:", ImageName))
                logger.error(("Error:", message))
                return None
        return images
    
    
    ## TODO
    # add a animation sheet loader and splicer
        
        
    # Todo: 
    # Add support for other image formats like JPG, GIF, and BMP
    # Add Animation, and Animation Player
    

        
        
def get_angle(point1: tuple, point2:tuple) -> float:
    """Calculate the angle in degrees between two points."""
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg



class Sound:
    def __init__(self):
        self.current_sound = None  # Track the currently playing sound
        self.stop_music = False

    def _load_sound(self, sound_name, type):
        # Try loading the sound with both .wav and .mp3 extensions
        for extension in ['wav', 'mp3']:
            sound_file = f"./assets/{type}/{sound_name}.{extension}"
            try:
                return pygame.mixer.Sound(sound_file)
            except pygame.error:
                continue
            except FileNotFoundError:
                continue
        logger.error(f"Sound file for {sound_name} with .wav or .mp3 extension not found.")

    def PlayFX(self, sound_name, volume=0.1):
        try:
            self.current_sound = self._load_sound(sound_name, "fx")
            self.current_sound.set_volume(volume)
            self.current_sound.play()
        except pygame.error as e:
            logger.error(f"Error playing sound {sound_name}: {e}")

    def PlaySound(self, sound_name, volume=0.5):
        try:
            if self.current_sound and self.current_sound.get_num_channels() > 0:
                # Sound is still playing, so do not start it again
                return

            self.current_sound = self._load_sound(sound_name, "music")
            self.current_sound.set_volume(volume)
            self.current_sound.play()
        except pygame.error as e:
            logger.error(f"Error playing sound {sound_name}: {e}")
            
    def PlayMusicRandom(self, volume=0.5):
        if self.stop_music:
            return
        try:
            music_folder = "./assets/music"
            music_files = [f for f in os.listdir(music_folder) if f.endswith('.wav') or f.endswith('.mp3')]

            if not music_files:
                logger.warn("No music files found in the music folder")

            random_music_file = random.choice(music_files)
            sound_name, _ = os.path.splitext(random_music_file)

            if self.current_sound and self.current_sound.get_num_channels() > 0:
                # Sound is still playing, so do not start it again
                return
            
            logger.log(f"Playeing Random song [ {sound_name} ]")

            self.current_sound = self._load_sound(sound_name, type="music")
            self.current_sound.set_volume(volume)
            self.current_sound.play()
        except pygame.error as e:
            logger.error(f"Error playing random music: {e}")
            
    def set_music_status(self, status=True):
        self.current_sound.stop()
        self.stop_music = not status
        
            
            

        
    
# TODO:
# Make UI Elements

#def draw_button(screen, color, rect, text):
#    pygame.draw.rect(screen, color, rect)
#    text_surface = font.render(text, True, TEXT_COLOR)
#    text_rect = text_surface.get_rect(center=rect.center)
#    screen.blit(text_surface, text_rect)



#
#    class Bullet:
#        def __init__(self, x, y, target, damage):
#            self.x = x
#            self.y = y
#            self.position = (x,y)
#            self.target = target
#            self.damage = damage
#            self.speed = 5
#    
#        def move(self):
#            target_x, target_y = self.target.x, self.target.y
#            dx, dy = target_x - self.x, target_y - self.y
#            dist = math.sqrt(dx ** 2 + dy ** 2)
#            if dist != 0:
#                self.x += self.speed * dx / dist
#                self.y += self.speed * dy / dist
#    
#        def draw(self, screen):
#            pygame.draw.circle(screen, COLOR.BLACK, (int(self.x), int(self.y)), 5)
#            
#


class UI:
    def __init__(self):
        pygame.font.init()
        self.scroll_areas = []

    def new_scroll_area(self, position=(50, 50), size=(200, 300), backround_color=(50,50,50), texture=None):
        scroll_area = self.ScrollArea(position, size, backround_color, texture)
        self.scroll_areas.append(scroll_area)
        return scroll_area

    def draw(self, surface):
        for scroll_area in self.scroll_areas:
            scroll_area.draw(surface)

    def handle_event(self, event):
        
        for scroll_area in self.scroll_areas:
            scroll_area.handle_event(event)
            

    class ScrollArea:
        def __init__(self, position, size, backround_color, texture= None):
            self.texture = texture
            if texture:
                self.texture = pygame.transform.scale(texture, size)
            self.position = position
            self.size = size
            self.backround_color = backround_color
            self.buttons = []
            self.scroll_offset = 0
            self.surface = pygame.Surface(size)
            self.rect = pygame.Rect(position, size)
            self.font = pygame.font.SysFont("Contage", 36)

        def new_button(self, text="Button", callback=None, colums=1, texture=None):
            button_position = (0, len(self.buttons) * 50)
            button_size = (self.size[0], 50)
            button = UI.Button(text, button_position, button_size, callback, texture=texture)
            self.buttons.append(button)
            return button

        def draw(self, surface):
            # Fill the scroll area surface with the background color or texture
            if not self.texture:
                self.surface.fill(self.background_color)
            else:
                self.surface.blit(self.texture, (0, 0))

            # Draw buttons with proper scrolling
            for index, button in enumerate(self.buttons):
                button.rect.y = button.position[1] - self.scroll_offset + (index *5)
                if 0 <= button.rect.y < self.size[1]:
                    button.draw(self.surface)

            # Blit the scroll area surface onto the main surface
            surface.blit(self.surface, self.position)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    for button in self.buttons:
                        button.handle_event(event, self.position, self.scroll_offset)
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y * 10
                self.scroll_offset = max(0, min(self.scroll_offset, len(self.buttons) * 50 - self.size[1]))
            

    class Button:
        def __init__(self, text, position, size, callback=None, color=(100,100,100), texture=None, selected_texture = None, selected_color = (150,150,150)):
            self.texture = texture
            self.selected_texture = selected_texture
            
            
            if texture:
                self.surface = pygame.transform.scale(texture, size)
            if selected_texture:
                self.sellected_surface = pygame.transform.scale(selected_texture, size)
            
            
            self.surface = pygame.Surface(size)
            self.sellected_surface = pygame.Surface(size)
            self.text = text
            self.position = position
            self.size = size
            self.callback = callback
            self.rect = pygame.Rect(position, size)
            self.font = pygame.font.SysFont("Contage", 36)
            self.color = (100, 100, 100)
            self.selected_color = selected_color
            self.selected = False
            
            

        def draw(self, surface):
            if self.texture:
                surface.blit(self.texture, self.texture.get_rect(center=self.rect.center))
                
            else:
                
                pygame.draw.rect(surface, self.color, self.rect)
            if self.text and self.text != "": 
                text_surface = self.font.render(self.text, True, (255, 255, 255))
            
                text_rect = text_surface.get_rect(center=self.rect.center)
                surface.blit(text_surface, text_rect)

        def handle_event(self, event, scroll_area_position, scroll_offset):
            # Adjust the event position to the scroll area's position and scroll offset
            adjusted_pos = (event.pos[0] - scroll_area_position[0], event.pos[1] - scroll_area_position[1] + scroll_offset)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(adjusted_pos):
                if self.callback:
                    self.callback()
                    
        def toggle_sellected(self):
            """Toggles the Button sellected state"""
            self.selected = not self.selected
            


import pygame

class Terminal:
    def __init__(self, position, input=False, callback=None, history_rows=5):
        self.position = position
        self.surface = pygame.Surface((500, 200))
        self.rect = pygame.Rect(position, (500, 200))
        self.font = pygame.font.SysFont("Arial", 24)
        self.input = input
        self.text_input = ""
        self.history = []
        self.history_index = 0
        self.active = False
        self.callback = callback
        self._cursor_blink_timer = 0
        self._cursor_visible = True  
        self.history_rows = history_rows
        
    def _split_string_at_index(self, input_string, index):
        array1 = input_string[:index]
        array2 = input_string[index:]
        return array1, array2

    def draw(self, screen,deltatime=0.01):
        self.update_cursor(deltatime)
        
        # Draw background box
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, (30, 30, 30), self.rect, 3)  # Outline
        
        # Draw text input area
        input_area = pygame.Rect(self.position[0] + 10, self.position[1] + 10, self.rect.width - 20, 30)
        pygame.draw.rect(screen, (100, 100, 100), input_area)
        pygame.draw.rect(screen, (80, 80, 80), input_area, 2)  # Input area outline
        
        # Render text input
        input_text = self.font.render(self.text_input, True, (255, 255, 255))
        screen.blit(input_text, (input_area.x + 5, input_area.y + 5))
        
        # Draw cursor (blinking)
        if self.active and self._cursor_visible:
            cursor_x = input_area.x + 5 + input_text.get_width()
            cursor_y = input_area.y + 5
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + input_text.get_height()), 2)
        
        # Draw text area for history
        text_area = pygame.Rect(self.position[0] + 10, self.position[1] + 50, self.rect.width - 20, self.rect.height - 60)
        pygame.draw.rect(screen, (70, 70, 70), text_area)
        pygame.draw.rect(screen, (50, 50, 50), text_area, 2)  # Text area outline
        
        # Render history lines
        line_y = text_area.y + 5
        for line in self.history[:self.history_rows]:  # Show last 10 lines
            if len(line) >= 37:
                line, overflow = self._split_string_at_index(line, 36)
            line_text = self.font.render(line, True, (255, 255, 255))
            screen.blit(line_text, (text_area.x + 5, line_y))
            line_y += 25  # Adjust spacing between lines

    def print_text(self, text:str) -> None:
        """Prints text to the Terminal

        Args:
            text (str): text to print
        """
        self.history = [text] + self.history

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if self.input:
                if event.key == pygame.K_RETURN:
                    # Execute command or add text to history
                    if self.callback:
                        self.callback(self.text_input)
                    self.text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                else:
                    self.text_input += event.unicode

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse clicked inside input area
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if self.active and event.type == pygame.KEYDOWN:
            self.update(event)

    def update_cursor(self, deltatime):
        self._cursor_blink_timer += 100 * (deltatime+1)
        if self._cursor_blink_timer >= 500:  # Blink every 500 milliseconds
            self._cursor_visible = not self._cursor_visible
            self._cursor_blink_timer = 0




