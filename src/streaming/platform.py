"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import (date, datetime, timedelta)
from streaming.users import PremiumUser

class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

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
        premium_users = []
        now = datetime.now()
        start = now - timedelta(days)
        total_tracks = 0

        for user in self._users.values():
            if isinstance(user, PremiumUser):
                premium_users.append(user)
        if len(premium_users) ==0:
            return 0.0

        for user in premium_users:
            unique_tracks = []
            for session in self._sessions:
                if session.user == user:
                    if session.timestamp >= start and session.timestamp <= now:
                        track = session.track
                        if track not in unique_tracks:
                            unique_tracks.append(track)
            total_tracks += len(unique_tracks)
        average = total_tracks /len(premium_users)
        return average


    def track_with_most_distinct_listeners(self):
        listeners = {}
        most_listened = 0
        most_distinct_listeners = None
        if len(self._sessions) == 0:
            return None

        for session in self._sessions:
            track = session.track
            user = session.user
            if track not in listeners:
                listeners[track] = []
            if user not in listeners[track]:
                listeners[track].append(user)

        for track in listeners:
            count = len(listeners[track])
            if count > most_listened:
                most_listened = count
                most_distinct_listeners = track
        return most_distinct_listeners








