from six import iteritems
from datetime import datetime
from time import mktime

class Song:
    """
    Song Attributes:
    name (String)
    track_id (Integer)
    artist (String)
    album_artist (String)
    composer = None (String)
    album = None (String)
    genre = None (String)
    kind = None (String)
    size = None (Integer)
    total_time = None (Integer)
    start_time = None (Integer)
    stop_time = None (Integer)
    track_number = None (Integer)
    track_count = None (Integer)
    disc_number = None (Integer)
    disc_count = None (Integer)
    year = None (Integer)
    date_modified = None (Time)
    date_added = None (Time)
    bit_rate = None (Integer)
    sample_rate = None (Integer)
    comments = None (String)
    rating = None (Integer)
    rating_computed = False (Boolean)
    album_rating = None (Integer)
    play_count = None (Integer)
    location = None (String)
    location_escaped = None (String)
    compilation = False (Boolean)
    grouping = None (String)
    lastplayed = None (Time)
    skip_count = None (Integer)
    skip_date = None (Time)
    persistent_id = None (String)
    album_rating_computed = False (Boolean)
    work = None (String)
    movement_name = None (String)
    movement_number = None (Integer)
    movement_count = None (Integer)
    playlist_only = None (Bool)
    apple_music = None (Bool)
    protected = None (Bool)
    """
    name = None
    track_id = None
    artist = None
    album_artist = None
    composer = None
    album = None
    genre = None
    kind = None
    size = None
    total_time = None
    start_time = None
    stop_time = None
    track_number = None
    track_count = None
    disc_number = None
    disc_count = None
    year = None
    date_modified = None
    date_added = None
    bit_rate = None
    sample_rate = None
    comments = None
    rating = None
    rating_computed = None
    album_rating = None
    play_count = None
    skip_count = None
    skip_date = None
    location = None
    location_escaped = None
    compilation = None
    grouping = None
    lastplayed = None
    persistent_id = None
    album_rating_computed = None
    work = None
    movement_name = None
    movement_number = None
    movement_count = None
    playlist_only = None
    apple_music = None
    protected = None

    def __iter__(self):
        for attr, value in iteritems(self.__dict__):
            yield attr, value

    def ToDict(self):
        return {key: value for (key, value) in self}

    def to_formatted_dict(self):
        """
        Returns dictionary with keys identical to the original XML format.
        """
        # Dictionary mapping variable names to formal names.
        formal_names = {'name': 'Name',
                        'work': 'Work',
                        'movement_number': 'Movement Number',
                        'movement_count': 'Movement Count',
                        'movement_name': 'Movement Name',
                        'track_id': 'Track ID',
                        'artist': 'Artist',
                        'album_artist': 'Album Artist',
                        'composer': 'Composer',
                        'album': 'Album',
                        'genre': 'Genre',
                        'kind': 'Kind',
                        'size': 'Size',
                        'total_time': 'Total Time',
                        'start_time': 'Start Time',
                        'stop_time': 'Stop Time',
                        'track_number': 'Track Number',
                        'track_count': 'Track Count',
                        'disc_number': 'Disc Number',
                        'disc_count': 'Disc Count',
                        'year': 'Year',
                        'date_modified': 'Date Modified',
                        'date_added': 'Date Added',
                        'bit_rate': 'Bit Rate',
                        'sample_rate': 'Sample Rate',
                        'comments': 'Comments',
                        'rating': 'Rating',
                        'rating_computed': 'Rating Computed',
                        'play_count': 'Play Count',
                        'album_rating': 'Album Rating',
                        'album_rating_computed': 'Album Rating Computed',
                        'persistent_id': 'Persistent ID',
                        'location_escaped': 'Location',
                        'compilation': 'Compilation',
                        'lastplayed': 'Play Date UTC',
                        'skip_count': 'Skip Count',
                        'skip_date': 'Skip Date',
                        'track_type': 'Track Type',
                        'grouping': 'Grouping',
                        'podcast': 'Podcast',
                        'movie': 'Movie',
                        'has_video': 'Has Video',
                        'loved': 'Loved',
                        'album_loved': 'Album Loved',
                        'playlist_only': 'Playlist Only',
                        'apple_music': 'Apple Music',
                        'protected': 'Protected'
                        }

        result = {}
        for key, value in self:
            if value is not None and value is not False:
                if key == 'location':
                    # Only escaped locations are used
                    continue
                if key in ['date_modified', 'date_added', 'lastplayed', 'skip_date']:
                    # Convert to datetime object
                    result[formal_names[key]] = datetime.fromtimestamp(mktime(value))
                else:
                    # No conversion necessary
                    result[formal_names[key]] = value

        return result
