import logging
import plistlib
from six import PY2
from six.moves.urllib import parse as urlparse
import time
from datetime import datetime
import io
import re

from libpytunes.Song import Song
from libpytunes.Playlist import Playlist


logger = logging.getLogger(__name__)

try:
    import xspf
    xspfAvailable = True
except ImportError:
    xspfAvailable = False
    pass


class Library:
    def __init__(self, itunesxml, musicPathXML=None, musicPathSystem=None, filesOnly=False):
        # musicPathXML and musicPathSystem will do path conversion
        # when xml is being processed on different OS then iTunes
        self.musicPathXML = musicPathXML
        self.musicPathSystem = musicPathSystem
        self.filesOnly = filesOnly
        with open(itunesxml, "rb") as fp:
            self.il = plistlib.load(fp, fmt=plistlib.FMT_XML)  # Much better support of xml special characters
        self.songs = {}
        self.getSongs()

    def getSongs(self):
        format = "%Y-%m-%d %H:%M:%S"
        for trackid, attributes in self.il['Tracks'].items():
            s = Song()

            s.track_id = int(attributes.get('Track ID')) if attributes.get('Track ID') else None
            s.size = int(attributes.get('Size')) if attributes.get('Size') else None

            # Timing
            s.total_time = int(attributes.get('Total Time')) if attributes.get('Total Time') else None
            s.start_time = int(attributes.get('Start Time')) if attributes.get('Start Time') else None
            s.stop_time = int(attributes.get('Stop Time')) if attributes.get('Stop Time') else None

            # Disc/track info
            s.disc_number = int(attributes.get('Disc Number')) if attributes.get('Disc Number') else None
            s.disc_count = int(attributes.get('Disc Count')) if attributes.get('Disc Count') else None
            s.track_number = attributes.get('Track Number')
            s.track_count = int(attributes.get('Track Count')) if attributes.get('Track Count') else None
            s.year = int(attributes.get('Year')) if attributes.get('Year') else None
            s.bpm = int(attributes.get('BPM')) if attributes.get('BPM') else None
            s.date_modified = time.strptime(str(attributes.get('Date Modified')), format) if attributes.get(
                'Date Modified') else None
            s.date_added = time.strptime(str(attributes.get('Date Added')), format) if attributes.get(
                'Date Added') else None
            s.bit_rate = int(attributes.get('Bit Rate')) if attributes.get('Bit Rate') else None
            s.sample_rate = int(attributes.get('Sample Rate')) if attributes.get('Sample Rate') else None
            s.volume_adjustment = int(attributes.get('Volume Adjustment')) if attributes.get(
                'Volume Adjustment') else None

            # Play and skip stats
            s.play_count = int(attributes.get('Play Count')) if attributes.get('Play Count') else None
            s.lastplayed = time.strptime(str(attributes.get('Play Date UTC')), format) if attributes.get(
                'Play Date UTC') else None
            s.skip_count = int(attributes.get('Skip Count')) if attributes.get('Skip Count') else None
            s.skip_date = time.strptime(str(attributes.get('Skip Date')), format) if attributes.get(
                'Skip Date') else None

            # Rating
            s.rating = int(attributes.get('Rating')) if attributes.get('Rating') else None
            s.rating_computed = 'Rating Computed' in attributes
            s.loved = 'Loved' in attributes
            s.disliked = 'Disliked' in attributes

            # Is part of compilation?
            s.compilation = 'Compilation' in attributes

            # Internal metadata
            s.artwork_count = int(attributes.get('Artwork Count')) if attributes.get('Artwork Count') else None
            s.persistent_id = attributes.get('Persistent ID')
            s.track_type = attributes.get('Track Type')
            s.file_folder_count = int(attributes.get('File Folder Count')) if attributes.get(
                'File Folder Count') else None
            s.library_folder_count = int(attributes.get('Library Folder Count')) if attributes.get(
                'Library Folder Count') else None

            # Actual track info
            s.name = attributes.get('Name')
            s.artist = attributes.get('Artist')
            s.album_artist = attributes.get('Album Artist')
            s.composer = attributes.get('Composer')
            s.album = attributes.get('Album')
            s.grouping = attributes.get('Grouping')
            s.genre = attributes.get('Genre')
            s.kind = attributes.get('Kind')

            # More iTunes specific stuff
            s.equalizer = attributes.get('Equalizer')
            s.comments = attributes.get('Comments')
            s.sort_album = attributes.get('Sort Album')
            if attributes.get('Location'):
                s.location_escaped = attributes.get('Location')
                s.location = s.location_escaped
                s.location = urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path[1:])
                s.location = s.location.decode('utf-8') if PY2 else s.location  # fixes bug #19
                if (self.musicPathXML is not None and self.musicPathSystem is not None):
                    s.location = s.location.replace(self.musicPathXML, self.musicPathSystem)

            # All fields below are fields I don't know the position of
            s.album_rating = attributes.get('Album Rating')
            s.album_rating_computed = 'Album Rating Computed' in attributes

            # Support classical music naming (Work+Movement Number+Movement Name) since iTunes 12.5
            s.work = attributes.get('Work')
            s.movement_number = attributes.get('Movement Number')
            s.movement_count = attributes.get('Movement Count')
            s.movement_name = attributes.get('Movement Name')

            s.podcast = 'Podcast' in attributes
            s.movie = 'Movie' in attributes
            s.has_video = 'Has Video' in attributes
            s.album_loved = 'Album Loved' in attributes
            s.playlist_only = 'Playlist Only' in attributes
            s.apple_music = 'Apple Music' in attributes
            s.protected = 'Protected' in attributes

            self.songs[int(trackid)] = s

    def getPlaylistNames(self, ignoreList=(
        "Library", "Music", "Movies", "TV Shows", "Purchased", "iTunes DJ", "Podcasts"
    )):
        playlists = []
        for playlist in self.il['Playlists']:
            if playlist['Name'] not in ignoreList:
                playlists.append(playlist['Name'])
        return playlists

    def getPlaylist(self, playlistName):
        for playlist in self.il['Playlists']:
            if playlist['Name'] == playlistName:
                # id 	playlist_id 	track_num 	url 	title 	album 	artist 	length 	uniqueid
                p = Playlist(playlistName)
                p.playlist_id = playlist['Playlist ID']
                p.is_folder = playlist.get('Folder', False)
                p.playlist_persistent_id = playlist.get('Playlist Persistent ID')
                p.parent_persistent_id = playlist.get('Parent Persistent ID')
                p.distinguished_kind = playlist.get('Distinguished Kind')
                p.is_genius_playlist = True if playlist.get('Genius Track ID') else False
                p.is_smart_playlist = True if playlist.get('Smart Info') and not playlist.get('Folder', False) else False
                tracknum = 1
                # Make sure playlist was not empty
                if 'Playlist Items' in playlist:
                    for track in playlist['Playlist Items']:
                        id = int(track['Track ID'])
                        t = self.songs[id]
                        t.playlist_order = tracknum
                        tracknum += 1
                        p.tracks.append(t)
                return p

    def getPlaylistxspf(self, playlistName):
        global xspfAvailable
        if (xspfAvailable):
            x = xspf.Xspf()
            for playlist in self.il['Playlists']:
                if playlist['Name'] == playlistName:
                    x.title = playlistName
                    x.info = ""
                    for track in playlist['Playlist Items']:
                        id = int(track['Track ID'])
                        x.add_track(title=self.songs[id].name, creator="", location=self.songs[id].location)
                    return x.toXml()
        else:
            logger.warning("xspf library missing, go to https://github.com/alastair/xspf to install.")
            return None

    def writeToXML(self, filepath, *, reformat=False):
        """
        Write the contents of `self.songs` to the specified XML filepath.

        This function does not consider changes to playlists.

        If `reformat` is true, newlines after certain tags are removed
        to more closely match the original XML generated by iTunes. However,
        some formatting (such as the width of <data> fields) is dictated by
        plistlib, and is outside the scope of this function.
        """
        # Begin by creating the Songs dictionary that will overwrite
        # the existing Tracks dictionary in `self.il`
        tracks_dict = {}
        for track_id, song_object in self.songs.items():
            tracks_dict[str(track_id)] = song_object.to_formatted_dict()

        # Replace the existing dictionary
        self.il["Tracks"] = tracks_dict

        # Update "Date" field
        self.il["Date"] = datetime.utcnow()

        # Write to XML, formatting if necessary
        # To retain the original order of the keys, sort_keys = False
        if not reformat:
            with open(filepath, 'wb') as outfile:
                plistlib.dump(self.il, outfile, sort_keys=False)
        else:
            file_object = io.BytesIO()
            plistlib.dump(self.il, file_object, sort_keys=False)
            file_object.seek(0)
            contents = file_object.read().decode()
            # this is probably the closest the data can get to being identically formatted to iTunes
            # python puts different line length on <data> fields
            # dict, data, and arrays have line breaks
            contents = re.sub(r'<\/key>\n\t*(?!\t*<dict>)(?!\t*<data>)(?!\t*<array>)', '</key>', contents)
            with open(filepath, 'w') as outfile:
                outfile.write(contents)
