"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import date, datetime, timedelta

class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._catalogue: dict[str, Track]= {}
        self._users: dict[str,User]= {}
        self._artists: dict[str, Artists]= {}
        self._albums: dict[str, Album]= {}
        self._playlists: dict[str, Playlist]= {}
        self._sessions: list[ListeningSession]= []

    def add_track(self, track):
        self._catalogue[track.track_id] = track

    def add_user(self, user):
        self._users[user.user_id] = user

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)

    def get_track(self,track_id):
        return self._catalogue.get(track_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self._catalogue.values())



    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_seconds =0
        for session in self._sessions:
            session_time = session.timestamp
            if session_time >= start and session_time <= end:
                total_seconds += session.duration_listened_seconds
        total_minutes = total_seconds / 60
        return total_minutes

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        pass




