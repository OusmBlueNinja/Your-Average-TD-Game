import pygame, time, math, datetime, os, sys, random

pygame.font.init()


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


def __init__(screen_size: tuple):
    global _SCREEN_SIZE, _SCREEN_HEIGHT, _SCREEN_WIDTH
    _SCREEN_SIZE = screen_size
    
    _SCREEN_HEIGHT, _SCREEN_WIDTH = _SCREEN_SIZE
    
    logger.log(f"Initializing screen size [ {screen_size} ]")
    
    logger.log(f"Creating Engine Folder")
    
    os.makedirs("./assets/images", exist_ok=True)
    os.makedirs("./assets/music", exist_ok=True)
    os.makedirs("./assets/fx", exist_ok=True)
    os.makedirs("./assets/icon", exist_ok=True)
    
    icon_folder = "./assets/icon"
    icon_file = [f for f in os.listdir(icon_folder) if f.endswith('.png')]
    if not icon_file:
        logger.warn("No Icon Found")
    else:
        pygame.display.set_icon(Image().LoadIcon(icon_file[0]))
        

    
    





font_Calibri = pygame.font.SysFont("Calibri", 36)

class FlashMessage:
    def __init__(self, screen, message, duration=2.5):
        self.screen = screen
        self.message = message
        self.duration = duration
        self.start_time = None
        self.active = False
        self.text_surface = font_Calibri.render(self.message, True, COLOR.BLACK)
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
    font_Calibri = pygame.font.SysFont("Calibri", size)
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
    
    
def get_mouse_pos():
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
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Update age
        self.age += 1
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
    
    
class Image:
    def LoadImage(self, ImageName):
        try:
            logger.log(f"Loading Image: %s" % ImageName)
            return pygame.image.load(f"./assets/images/{ImageName}.png")
        except pygame.error as message:
            logger.error(("Unable to load image:", ImageName))
            logger.error(("Error:", message))
            return None
        
    def LoadIcon(self, IconName):
        try:
            logger.log(f"Loading Image: %s" % IconName)
            return pygame.image.load(f"./assets/icon/{IconName}")
        except pygame.error as message:
            logger.error(("Unable to load icon:", IconName))
            logger.error(("Error:", message))
            return None
        
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
        
    
