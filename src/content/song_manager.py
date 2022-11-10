import json
import os

from content.song import Song


# true to debug and False to release
if True:
    keys_folder = 'src\\content\\assets\\song_keys'
    songs_folder = 'src\\content\\assets\\songs'
else:
    keys_folder = 'song_keys'
    songs_folder = 'songs'

# the list of filepaths in keys_folder
songs_keys = [f'{keys_folder}\\{json_file}' for json_file in os.listdir(keys_folder)]



def get_song(index):
    """Gets a song from keys_folder based on the index.

    Args:
        index (int): The index of the song to select.

    Returns:
        Song: A song object containig the chosen song file_path.
    """
    _file_path = songs_keys[index]
    _json = json.load(open(_file_path))
    
    _song = Song(f'{songs_folder}\\{_json["file_name"]}',
                 bpm = _json['bpm'],
                 title = _json['title'],
                 artist = _json['artist'],
                 key_map = _json['key_map'])
    return _song

