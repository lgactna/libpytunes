from six import iteritems
from datetime import datetime
from time import mktime

class Song:
    """
    Song Attributes:
    track_id (Integer)
    size = None (Integer)
    total_time = None (Integer)
    start_time = None (Integer)
    stop_time = None (Integer)
    disc_number = None (Integer)
    disc_count = None (Integer)
    track_number = None (Integer)
    track_count = None (Integer)
    year = None (Integer)
    bpm = None (Integer)
    date_modified = None (Time)
    date_added = None (Time)
    bit_rate = None (Integer)
    sample_rate = None (Integer)
    volume_adjustment = None (Integer)
    rating = None (Integer)
    rating_computed = False (Boolean)
    play_count = None (Integer)
    lastplayed = None (Time)
    skip_count = None (Integer)
    skip_date = None (Time)
    loved = False (Boolean)
    disliked = False (Boolean)
    compilation = False (Boolean)
    artwork_count = None (Integer)
    persistent_id = None (String)
    track_type = None (String)
    file_folder_count = None (Integer)
    library_folder_count = None (Integer)
    name (String)
    artist (String)
    album_artist (String)
    composer = None (String)
    album = None (String)
    grouping = None (String)
    genre = None (String)
    kind = None (String)
    equalizer = None (String)
    comments = None (String)
    sort_album = None (String)
    location = None (String)
    location_escaped = None (String)

    album_rating = None (Integer)
    album_rating_computed = False (Boolean)
    work = None (String)
    movement_name = None (String)
    movement_number = None (Integer)
    movement_count = None (Integer)

    podcast = False (Boolean)
    movie = False (Boolean)
    has_video = False (Boolean)
    album_loved = False (Boolean)
    playlist_only = False (Boolean)
    apple_music = False (Boolean)
    protected = False (Boolean)
    """
    track_id = None
    size = None
    total_time = None
    start_time = None
    stop_time = None
    disc_number = None
    disc_count = None
    track_number = None
    track_count = None
    year = None
    bpm = None
    date_modified = None
    date_added = None
    bit_rate = None
    sample_rate = None
    volume_adjustment = None
    play_count = None
    lastplayed = None
    skip_count = None
    skip_date = None
    rating = None
    rating_computed = None
    loved = None
    disliked = None
    compilation = None
    artwork_count = None
    persistent_id = None
    track_type = None
    file_folder_count = None
    library_folder_count = None
    name = None
    artist = None
    album_artist = None
    composer = None
    album = None
    grouping = None
    genre = None
    kind = None
    equalizer = None #
    comments = None
    sort_album = None
    location = None
    location_escaped = None

    # All fields below are fields I do not know the typical position of.
    album_rating = None
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
        formal_names = {'track_id': 'Track ID',
                        'size': 'Size',
                        'total_time': 'Total Time',
                        'start_time': 'Start Time',
                        'stop_time': 'Stop Time',
                        'disc_number': 'Disc Number',
                        'disc_count': 'Disc Count',
                        'track_number': 'Track Number',
                        'track_count': 'Track Count',
                        'year': 'Year',
                        'bpm': 'BPM',
                        'date_modified': 'Date Modified',
                        'date_added': 'Date Added',
                        'bit_rate': 'Bit Rate',
                        'sample_rate': 'Sample Rate',
                        'volume_adjustment': 'Volume Adjustment',
                        'play_count': 'Play Count',
                        'lastplayed': 'Play Date UTC',
                        'skip_count': 'Skip Count',
                        'skip_date': 'Skip Date',
                        'rating': 'Rating',
                        'rating_computed': 'Rating Computed',
                        'loved': 'Loved',
                        'disliked': 'Disliked',
                        'compilation': 'Compilation',
                        'artwork_count': 'Artwork Count',
                        'persistent_id': 'Persistent ID',
                        'track_type': 'Track Type',
                        'file_folder_count': 'File Folder Count',
                        'library_folder_count': 'Library Folder Count',
                        'name': 'Name',
                        'artist': 'Artist',
                        'album_artist': 'Album Artist',
                        'composer': 'Composer',
                        'album': 'Album',
                        'grouping': 'Grouping',
                        'genre': 'Genre',
                        'kind': 'Kind',
                        'equalizer': 'Equalizer',
                        'comments': 'Comments',
                        'sort_album': 'Sort Album',
                        'location_escaped': 'Location',
                        'album_rating': 'Album Rating',
                        'album_rating_computed': 'Album Rating Computed',
                        'work': 'Work',
                        'movement_number': 'Movement Number',
                        'movement_count': 'Movement Count',
                        'movement_name': 'Movement Name',
                        'podcast': 'Podcast',
                        'movie': 'Movie',
                        'has_video': 'Has Video',
                        'album_loved': 'Album Loved',
                        'playlist_only': 'Playlist Only',
                        'apple_music': 'Apple Music',
                        'protected': 'Protected',
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
