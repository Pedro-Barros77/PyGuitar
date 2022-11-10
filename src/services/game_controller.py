import pygame, sys
from pygame.locals import *

from utils import lists

# If the game is running, controls the game loop
playing = False

def handle_events(game):
    """Iterates through each event and call it's appropriate function.

    Args:
        game (Game): The currently running game.
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_app()
        elif event.type == KEYDOWN:
            handle_keydown(event.key, game)
        elif event.type == KEYUP:
            handle_keyup(event.key, game)
    
def handle_keydown(key, game):
    """Decides what to do with the key pressed by the user.

    Args:
        key (int): The pygame keycode of the key.
        game (Game): The currently running game.
    """
    if key in game.btn_keys:
        game.pressed_keys.append(key)
        key_index = game.btn_keys.index(key)
        target = lists.first_default([x for x in game.target_keys if x[0] == key_index], (0,0))
        if target in game.target_keys:
            if target not in game.caught_keys:
                game.caught_keys.append(target)
            game.target_keys.remove(target)
    
    if(key == K_r):
        restart(game)
    if(key == K_ESCAPE):
        quit_app()
    if(key == K_p):
        pass

def handle_keyup(key, game):
    """Decides what to do with the key released by the user.

    Args:
        key (int): The pygame keycode of the key.
        game (Game): The currently running game.
    """
    if key in game.btn_keys:
        game.pressed_keys.remove(key)


def restart(game):
    """Clears all game data and starts from beginning.

    Args:
        game (Game): The currently running game.
    """
    game.guitar_fret_offset = 0
    game.target_keys = []
    game.caught_keys = []
    game.drawer.clear()
    game.start()
    
def quit_app():
    """Stops the game and closes application.
    """
    pygame.display.quit()
    pygame.quit()
    sys.exit()