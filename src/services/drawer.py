import pygame
from pygame import mixer
import datetime


from utils.constants import colors
from utils import math, lists

class Drawer:
    
    def __init__(self, game):
        # the game to be drawn
        self.game = game
        
    #region Table
        # the size of the table (guitar neck)
        self.table_width = int(game.screen.get_size()[0] * 0.4)
        self.table_height = int(game.screen.get_size()[1] // 1.1)
        self.table_size = (self.table_width, self.table_height)
        # the space from left and top of the screen to the table (guitar neck)
        self.table_offset = math.space_to_center(self.table_size, self.game.screen.get_size())
        # increases the table height by it's y offset so it can be extended to the end of the screen
        self.table_height += self.table_offset[1]
        self.table_size = (self.table_width, self.table_height)
    #endregion
        
    #region Properties - control constants
        # the colors of each button, in order
        self.BTN_COLORS = [colors.GREEN_BTN, colors.RED_BTN, colors.YELLOW_BTN, colors.BLUE_BTN, colors.ORANGE_BTN]
        # the number of frets (horizontal lines)
        self.FRET_COUNT = 4
        # the thickness of the first string
        self.STRING_WIDTH = 5
        # the thickness of the frets
        self.FRET_WIDTH = 5
        
        # the diameter of guitar buttons and keys
        self.btn_diameter = self.table_width * 0.06
    #endregion
    
    #region ReadOnly - Value defined once on runtime
        # the width of the strings (vertical lines) from the thinnest to the thickest
        self.string_widths = []
        # the distance of the buttons to the top of the screen
        self.buttons_top = self.table_offset[1] + self.table_height - self.btn_diameter - ((self.table_width/5)//2)
        # the number of pixels to travel for each song millisecond
        self.px_per_ms = 0
        # the offset (in milliseconds) a key should appear before it's time to be hit
        self.key_show_offset = 0
    #endregion
    
    #region Control Variables - private variables
        # a float in a range of 0 to 1, defining the progress of the frets motion
        self.guitar_fret_offset = 0
    #endregion
        

    def draw_text(self, text, pos, color = colors.WHITE, size = 30, font = 'Arial'):
        text = str(text)
        
        r, g, b, *a = color
        color = (r,g,b)
        _font = None
        
        if type(font) == str:
            _font = pygame.font.SysFont(font, size)
        else:
            _font = font
                
        text_surface = _font.render(text, False, color)
        if len(a) > 0:
            text_surface.set_alpha(a[0])
        self.game.screen.blit(text_surface, pos)
        
    def time(self):
        return mixer.music.get_pos()

    def clear(self):
        self.string_widths = []
        self.px_per_ms = 0
        self.key_show_offset = 0

    def draw_table(self):
        def draw_plane():
            table = colors.horizontal_gradient(self.table_size, colors.add_evenly(colors.DARK_BROWN, -100), colors.DARK_BROWN)
            self.game.screen.blit(table, self.table_offset)
        
        def draw_frets():
            _fret_margin = self.table_height // self.FRET_COUNT + self.FRET_WIDTH
            _fret_overflow = 4
            _top = math.clamp(self.guitar_fret_offset * _fret_margin, 0, self.table_height*2)
            for _ in range(0, self.FRET_COUNT):
                _fret_shadow = pygame.Surface((self.table_width+_fret_overflow, self.FRET_WIDTH))
                _fret = pygame.Surface((self.table_width+_fret_overflow, self.FRET_WIDTH-2))
                _fret_shadow.fill(colors.add_evenly(colors.GRAY, -100))
                 
                
                _fret_offset = (self.table_offset[0]-(_fret_overflow//2), self.table_offset[1] + _top)
                self.game.screen.blit(_fret_shadow, _fret_offset)
                self.game.screen.blit(_fret, _fret_offset)
                _top += _fret_margin

                
        def draw_strings():
            self.string_margin = self.table_width / 5
            _left = self.string_margin //2
            _shadow_width = 2
            for i in range(0, 5):
                _string_w = self.STRING_WIDTH + i*2
                self.string_widths.append(_string_w)
                _line_shadow = pygame.Surface((_string_w, self.table_height))
                _line = pygame.Surface((self.STRING_WIDTH-_shadow_width + i*2, self.table_height))
                _line.fill(colors.GOLDEN_BROWN)
                _line_shadow.fill(colors.add_evenly(colors.GOLDEN_BROWN, -100))
                _line_offset = (self.table_offset[0] + _left, self.table_offset[1])
                self.game.screen.blit(_line_shadow, _line_offset)
                self.game.screen.blit(_line, (_line_offset[0]+_shadow_width//2, _line_offset[1]))
                _left += self.string_margin
                if i > 0:
                    _shadow_width += 2
        
        draw_plane()
        draw_frets()
        draw_strings()
        
        # change literal value by BPM calc
        _fret_offset = self.guitar_fret_offset + (self.game.tick_speed/48.3)
        if _fret_offset > 1:
            _fret_offset -= 1
                    
            
        self.guitar_fret_offset = _fret_offset
        
    
    def draw_buttons(self):
        _btn_margin = self.table_width/5
        _left = _btn_margin //2
            
        def get_pressed_color(i):
            if self.game.btn_keys[i] in self.game.pressed_keys:
                return colors.add_evenly(self.BTN_COLORS[i], 400)
            return colors.CARBON
        
        for i in range(0,5):
            _x_offset = self.table_offset[0] + _left + (self.string_widths[i]//2)
            _y_offset = self.table_offset[1] + self.table_height - self.btn_diameter - (_btn_margin//2)
            _btn_colored = pygame.draw.circle(self.game.screen, self.BTN_COLORS[i], (_x_offset, _y_offset), self.btn_diameter)
            _btn_silver = pygame.draw.circle(self.game.screen, colors.CARBON if self.game.btn_keys[i] in self.game.pressed_keys else colors.SILVER, (_x_offset, _y_offset), self.btn_diameter - (self.btn_diameter/5))
            _btn_hole = pygame.draw.circle(self.game.screen, get_pressed_color(i), (_x_offset, _y_offset), self.btn_diameter - (self.btn_diameter/2.5))
            
            _left += _btn_margin
        
        
        
    def draw_keymap(self, song):
        for (i,key) in enumerate(song.key_map):
            _time = key['time']
            _now = self.time()
            
            
            _show_time = (((_time * self.table_offset[1])/self.buttons_top) * 10) * self.game.tick_speed
            
            if self.key_show_offset == 0:
                self.key_show_offset = _time - _show_time
            
            if _time - self.key_show_offset > _now:
                continue
            
            _time_delta = _time - (_time - self.key_show_offset)
            _pxl_delta = self.buttons_top - self.table_offset[1]
            
            if self.px_per_ms == 0:
                self.px_per_ms = (_pxl_delta/_time_delta) 
            
            _y = self.px_per_ms * (_now-(_time - self.key_show_offset))
            
            _key_num = key['key']
            self.draw_key(_key_num, _y, _time)
    
    def draw_key(self, key_num, y, time, show_hitbox = False):
        if (key_num, time) in self.game.caught_keys:
            return
        _btn_margin = self.table_width/5
        _left = _btn_margin //2
        _x_offset = self.table_offset[0] + _left + (_btn_margin * key_num) + (self.string_widths[key_num]//2)
        _y_offset = y
        _target_error_margin = self.btn_diameter * 1.5
        
        if math.between(_y_offset, self.buttons_top - _target_error_margin, self.buttons_top + _target_error_margin) and (key_num, time) not in self.game.target_keys:
            self.game.target_keys.append((key_num, time))
            
        elif _y_offset - self.btn_diameter > self.buttons_top + self.btn_diameter and (key_num, time) in self.game.target_keys:
            self.game.target_keys.remove((key_num, time))
            
        _btn_silver = pygame.draw.circle(self.game.screen, colors.SILVER, (_x_offset, _y_offset), self.btn_diameter)
        _btn_colored = pygame.draw.circle(self.game.screen, self.BTN_COLORS[key_num], (_x_offset, _y_offset), self.btn_diameter - (self.btn_diameter/10))
        _btn_hole = pygame.draw.circle(self.game.screen, colors.CARBON, (_x_offset, _y_offset), self.btn_diameter - (self.btn_diameter/2))
        _btn_inner_silver = pygame.draw.circle(self.game.screen, colors.SILVER, (_x_offset, _y_offset), self.btn_diameter - (self.btn_diameter/1.5))
        
        if not show_hitbox: 
            return
        
        hitbox_diameter = (_y_offset + _target_error_margin) - (_y_offset - _target_error_margin)
        hitbox_center = (_x_offset, _y_offset)
        pygame.draw.circle(self.game.screen, colors.PURPLE, hitbox_center, hitbox_diameter/2, 10)
        
        pygame.draw.rect(self.game.screen, colors.GRAY, ((0, self.buttons_top - 5), (self.game.screen.get_size()[0], 10)))
        
        
    def draw_ui(self):
        _font_size = 30
        _margin_top = 10
        _top = 0
        _left = 20
        
        
        def draw_header():
            def pos():
                nonlocal _top
                _top += _margin_top + _font_size
                return (_left, _top)
            
            self.draw_text("Quick Restart: R", pos(), size=_font_size)
            self.draw_text("Quit app: ESQ", pos(), size=_font_size)
            
        def draw_keybinds():
            _keybind_font_size = 40
            _font = pygame.font.SysFont('Arial', _keybind_font_size)
            _keybind_top = self.buttons_top + 50
            _keybind_left = self.table_offset[0] + (self.table_width/5)//2
            for i in range(1,6):
                key = pygame.key.name(self.game.btn_keys[i-1]).upper()
                text_width, _ = _font.size(key)
                _new_color = self.fade_out(colors.WHITE, self.game.start_time, self.game.start_time + datetime.timedelta(seconds=4), 3500)
                self.draw_text(key, (_keybind_left - (text_width/2) + (self.string_widths[i-1]/2), _keybind_top), _new_color,_keybind_font_size)
                _keybind_left += self.table_width/5
            
        def draw_title():
            _title_size = 80
            _font = pygame.font.SysFont('Arial', _title_size)
            _text = f'{self.game._song.title} - {self.game._song.artist}'
            _text_width =_font.size(_text)[0]
            _left = (self.game.screen.get_size()[0] - _text_width)//2
            _top = 100
            self.draw_text(_text, (_left, _top),self.fade_out(colors.PURPLE, self.game.start_time, self.game.start_time + datetime.timedelta(seconds=4), 3500), _title_size, _font)
        
        
        draw_header()
        draw_title()
        draw_keybinds()
    

    def fade_out(self, color, start_time, end_time, offset = 0):
        now = datetime.datetime.now().timestamp()
        end = end_time.timestamp()
        start = (start_time + datetime.timedelta(milliseconds=offset)).timestamp()
        
        if start > now:
            return colors.add_alpha(color, 255)
        
        percentage = ((now - start) / (end - start)) * 100
        alpha = (255*(100-percentage))/100
        
        return colors.add_alpha(color, int(alpha))