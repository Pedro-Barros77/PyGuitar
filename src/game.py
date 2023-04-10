import pygame
from pygame.locals import *
from pygame import mixer
from datetime import datetime

from services.drawer import Drawer
from utils.constants import colors
from content import song_manager
from services import game_controller


class Game:
    def __init__(self):
        # pygame clock to control FPD
        self.clock = pygame.time.Clock()
        # drawer class to display the game on screen
        self.drawer = None
        # the main surface to hold all game drawings
        self.screen = None
        # the overall speed of the game
        self.tick_speed = 1.5
        # the list of currently pressed keys of keyboard
        self.pressed_keys = []
        # the keybind of each guitar button
        self.btn_keys = [K_a, K_s, K_j, K_k, K_l]
        # the datetime the game started
        self.start_time = None
        # the size of user's monitor/screen
        self.monitor_size = (0,0)
        # the keys that are under the buttons (ready to press and score) - (key_index, time)
        self.target_keys = [] 
        # the keys that the user successfully scored - (key_index, time)
        self.caught_keys = []
        
        
    
    def start(self):
        """Starts the game and the song from the beginning
        """
        pygame.init()
        if self.monitor_size == (0,0):
            self.monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h - 100)
        mixer.init()
        pygame.display.set_caption('Py-Guitar')
        
        #debug
        self._song = song_manager.get_song(0)
        mixer.music.load(self._song.file_path)
        mixer.music.set_volume(0.5)
        
        self.screen = pygame.display.set_mode(self.monitor_size)
        
        mixer.music.play()
        game_controller.playing = True
        
        self.start_time = datetime.now()
        self.drawer = Drawer(self)
        self.game_loop()

    def game_loop(self):
        """The main game loop
        """
        while game_controller.playing:
            self.clock.tick(60 * self.tick_speed)
            
            game_controller.handle_events(self)
            
            self.screen.fill(colors.BLACK)
            self.drawer.draw_table()
            self.drawer.draw_keymap(self._song)
            self.drawer.draw_buttons()
            
            self.drawer.draw_ui()
            pygame.display.update()
            
            # pygame.display.set_caption(str(mixer.music.get_pos()))
            
            
            




# from aubio import source, onset

# def get_onset_times(file_path):
#     window_size = 1024 # FFT size
#     hop_size = window_size // 4

#     sample_rate = 0
#     src_func = source(file_path, sample_rate, hop_size)
#     sample_rate = src_func.samplerate
#     onset_func = onset('default', window_size, hop_size)
    
#     duration = float(src_func.duration) / src_func.samplerate

#     onset_times = [] # seconds
#     while True: # read frames
#         samples, num_frames_read = src_func()
#         if onset_func(samples):
#             onset_time = onset_func.get_last_s()
#             if onset_time < duration:
#                 onset_times.append(onset_time)
#             else:
#                 break
#         if num_frames_read < hop_size:
#             break
    
#     return onset_times