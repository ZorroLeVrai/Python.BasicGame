import pygame
from sys import exit
from random import randint, choice
from enum import Enum

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
MAX_FRAMES_PER_SECOND = 60
GAME_TITLE = 'First Game'

GROUND_Y_POSITION = 300
FLY_ALTITUDE = 90
JUMP_SPEED = 15
GRAVITY = 0.5
ENEMY_SPEED = 6

BACK_GROUND_MUSIC = False
MUSIC_VOLUME = 0.1

GAME_SOUND = False
SOUND_VOLUME = 0.1


class Enemy(Enum):
    Snail = 1
    Fly = 2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1_surface = create_image_surface(
            'graphics/player/player_walk_1.png', True)
        player_walk2_surface = create_image_surface(
            'graphics/player/player_walk_2.png', True)
        self.player_walk = [player_walk1_surface, player_walk2_surface]
        self.player_state_index = 0
        self.player_jump_surface = create_image_surface(
            'graphics/player/jump.png', True)
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(SOUND_VOLUME)
        self.image = self.player_walk[self.player_state_index]
        self.rect = self.image.get_rect(midbottom=(80, GROUND_Y_POSITION))
        self.vspeed = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_Y_POSITION:
            self.vspeed = -1*JUMP_SPEED
            if GAME_SOUND:
                self.jump_sound.play()

    def apply_gravity(self):
        # simualte gravity
        self.vspeed += GRAVITY
        self.rect.y += self.vspeed
        if self.rect.bottom >= GROUND_Y_POSITION:
            self.rect.bottom = GROUND_Y_POSITION

    def animation_state(self):
        if (self.rect.bottom < GROUND_Y_POSITION):
            self.image = self.player_jump_surface
        else:
            self.player_state_index += 0.1
            if self.player_state_index >= len(self.player_walk):
                self.player_state_index = 0
            self.image = self.player_walk[int(self.player_state_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if (type == Enemy.Fly):
            fly_frame1 = create_image_surface(
                'graphics/fly/fly1.png', True)
            fly_frame2 = create_image_surface(
                'graphics/fly/fly2.png', True)
            self.frames = [fly_frame1, fly_frame2]
            y_pos = GROUND_Y_POSITION - FLY_ALTITUDE
        else:
            snail_frame1 = create_image_surface(
                'graphics/snail/snail1.png', True)
            snail_frame2 = create_image_surface(
                'graphics/snail/snail2.png', True)
            self.frames = [snail_frame1, snail_frame2]
            y_pos = GROUND_Y_POSITION

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index = 0 if self.animation_index else 1
        self.image = self.frames[self.animation_index]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= ENEMY_SPEED
        self.destroy()


def do_nothing(item, summary):
    """
    Only used for illustration purposes
    """
    pass


def create_font(font_file, font_size):
    """
    Create a new font
    :param font_file: the file containing the font
    :param size: the font size
    """
    return pygame.font.Font(font_file, font_size)


def create_plain_color_surface():
    """
    Create a plain color surface
    :return: a plain color surface
    """
    # Set the size of the surface
    surface_width = 100
    surface_heigth = 200
    plain_surface = pygame.Surface((surface_width, surface_heigth))

    # Set the color of the surface
    surface_color = 'Red'
    plain_surface.fill(surface_color)

    return plain_surface


def create_text_surface(font, text, anti_aliasing, color):
    """
    Create the text surface
    font: the font
    text: the text to dislay
    anti_aliasing: boolean to say if we want to smooth the display of the text
    color: the color of the text
    """
    return font.render(text, anti_aliasing, color)


def create_image_surface(image_path, convert_alpha=False):
    """
    Create an image surface
    :param image_path: the image path
    :param convert_alpha: boolean to specify if we want to use transparancy colors
    :return: an image surface
    """
    # convert() converts the image to a format pygame can work with easilly
    surface = pygame.image.load(image_path)
    if convert_alpha:
        return surface.convert_alpha()
    else:
        return surface.convert()


def block_transfer(surface, position):
    """
    Block Transfer - Copy a surface into the main surface
    :param surface: the surface to be transfered to the main surface (the surface to be displayed)
    :param position: is a (X,Y) tuple representing the X and Y coordinates that point where to display the surface
    """
    screen.blit(surface, position)


def create_rectangle_using_size(left, top, width, height):
    return pygame.Rect(left, top, width, height)


def collide_rectangle(rect1, rect2):
    """
    :return: true if there is a collision between rectangles
    false otherwise
    """
    return rect1.colliderect(rect2)


def collide_point(rect, point):
    """
    :return: true if there is a collision between a rectangle and a point
    false otherwise
    """
    return rect.collidepoint(point)


def get_mouse_position():
    return pygame.mouse.get_pos()


def get_mouse_button_pressed():
    return pygame.mouse.get_pressed()


def get_key_pressed():
    return pygame.key.get_pressed()


def draw_rectangle(surface, color, rectangle, width=0, border_radius=-1):
    pygame.draw.rect(surface, color, rectangle, width, border_radius)


def draw_line(surface, color, start_pos, end_pos, width):
    pygame.draw.line(surface, color, start_pos, end_pos, width)


def draw_ellipse(surface, color, rectangle):
    pygame.draw.ellipse(surface, color, rectangle)


def fill_surface_with_color(surface, color):
    surface.fill(color)


def end_game():
    pygame.quit()
    # exit the current program
    exit()


def display_score():
    global score
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score = current_time
    score_color = (64, 64, 64)
    score_surface = create_text_surface(
        score_font, f"Score: {current_time}", False, score_color)
    score_rect = score_surface.get_rect(center=(WINDOW_WIDTH / 2, 50))
    score_background_color = '#c0e8ec'
    draw_rectangle(screen, score_background_color, score_rect)
    screen.blit(score_surface, score_rect)


def init_game_state():
    global game_active, start_time
    game_active = True
    start_time = pygame.time.get_ticks()


def collision_sprite():
    # The last argument says if we want to kill our enemy sprite that is responsable for the collision
    is_collision = pygame.sprite.spritecollide(
        player.sprite, obstacle_group, False)
    if is_collision:
        obstacle_group.empty()
    return is_collision


def draw_game():
    global game_active

    block_transfer(sky_surface, (0, 0))
    block_transfer(ground_surface, (0, GROUND_Y_POSITION))

    display_score()

    # drawing and updating the player
    player.draw(screen)
    player.update()

    # obstacles
    obstacle_group.draw(screen)
    obstacle_group.update()

    # check for collision with enemies
    game_active = not collision_sprite()


def draw_game_not_active():
    fill_surface_with_color(screen, (94, 129, 162))
    screen.blit(player_stand_surface, player_stand_rect)
    screen.blit(game_name, game_name_rect)

    # put the player back on the ground
    player.sprite.rect.midbottom = (80, GROUND_Y_POSITION)

    if score == 0:
        screen.blit(game_message, game_message_rect)
    else:
        score_message = create_text_surface(score_font,
                                            f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(score_message, score_message_rect)


def handle_game_active_events(event, obstacle_timer):
    # using the game loop is much faster than calling the methods to handle events
    if event.type == obstacle_timer:
        enemy_type = choice([Enemy.Snail, Enemy.Fly])
        obstacle_group.add(Obstacle(enemy_type))

    match event.type:
        # triggered if we close the window
        case pygame.QUIT:
            end_game()

        # triggered if we move the mouse
        case pygame.MOUSEMOTION:
            do_nothing(event.pos, "get the mouse position")

        case pygame.MOUSEBUTTONDOWN:
            do_nothing(None, "mouse down")

        case pygame.MOUSEBUTTONUP:
            do_nothing(None, "mouse up")

        case pygame.KEYDOWN:
            do_nothing(None, "key down")

        case obstacle_timer:
            pass


def handle_game_notactive_events(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        init_game_state()


# Init pygame
pygame.init()

# Create the display surface with the given width and height
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Set the window tirtle
pygame.display.set_caption(GAME_TITLE)
# Get the clock object
clock = pygame.time.Clock()

score_font = create_font('font/Pixeltype.ttf', 50)
score = 0
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(MUSIC_VOLUME)
if BACK_GROUND_MUSIC:
    # loop the background music forever
    background_music.play(loops=-1)

# create a single group for the player
player = pygame.sprite.GroupSingle()
player.add(Player())

# create a group for the enemies
obstacle_group = pygame.sprite.Group()

# init sufaces
sky_surface = create_image_surface('graphics/Sky.png')
ground_surface = create_image_surface('graphics/ground.png')

# Intro screen
# player standing
player_stand_surface = create_image_surface(
    'graphics/player/player_stand.png', True)
player_stand_surface = pygame.transform.rotozoom(
    player_stand_surface, 0, 2)
player_stand_rect = player_stand_surface.get_rect(center=(400, 200))

game_name = create_text_surface(
    score_font, GAME_TITLE, False, (111, 196, 196))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = score_font.render('Press space to run', False, (111, 196, 196))
game_message_rect = game_message.get_rect(center=(400, 320))

# Timers - create custom user events
# timer to spawn new enemies
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# snail animation timer
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

# fly animation timer
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

init_game_state()

# the game loop - draw all our elements and update everything
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()

        if game_active:
            handle_game_active_events(event, obstacle_timer)
        else:
            handle_game_notactive_events(event)

    if game_active:
        draw_game()
    else:
        draw_game_not_active()

    # update the display surface
    pygame.display.update()

    # Set the ceiling of a maximum MAX_FRAMES_PER_SECOND frames per second
    clock.tick(MAX_FRAMES_PER_SECOND)
