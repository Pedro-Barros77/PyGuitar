class Song:
    def __init__(self, file_path, bpm, **kwargs):
        # the path of the song file to be played
        self.file_path = file_path
        # the BPM of the song
        self.bpm = bpm
        # the array of keys {time, key, duration}
            #time: the time (in milliseconds) of the song that the key is placed
            #key: the index of the key (0-4)
        self.key_map = kwargs.pop('key_map', [])
        # the title of the song
        self.title = kwargs.pop('title', 'unknown')
        # the artist of the song
        self.artist = kwargs.pop('artist', 'unknown')