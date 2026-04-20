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
from streaming.users import FamilyAccountUser
from streaming.playlists import CollaborativePlaylist

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


    def avg_session_duration_by_user_type(self)-> list[tuple[str, float]]:
        total = {}
        count ={}
        for session in self._sessions:
            user = session.user
            if isinstance(user, FamilyAccountUser):
                user_type = "FamilyAccountUser"
            elif isinstance(user, FreeUser):
                user_type = "FreeUser"
            elif isinstance(user, PremiumUser):
                user_type = "PremiumUser"
            elif isinstance(user, FamilyMember):
                user_type = "FamilyMember"

            duration = session.duration_listened_seconds
            if user_type not in total:
                total[user_type] = 0
                count[user_type] = 0
            total[user_type] += duration
            count[user_type] += 1
        avreges = []
        for user_type in total:
            avrege = total[user_type] / count[user_type]
            avreges.append((user_type, avrege))

        avreges.sort(key=lambda x: x[1], reverse= True)
        return avreges

    def total_listening_time_underage_sub_users_minutes(self):
        total_listening_time = 0
        for user in self._users.values():
            if isinstance(user, FamilyAccountUser):
                for sub_user in user.sub_users:
                    if sub_user.age < 18:
                        total_listening_time = total_listening_time + sub_user.total_listening_seconds()
        total_listening_minutes = total_listening_time / 60
        return total_listening_minutes


    def top_artists_by_listening_time(self, n: int = 5):
        list_of_artists = []
        for artist in self._artists.values():
            total = 0
            for session in self._sessions:
                track = session.track
                if isinstance(track,Song):
                    if track in artist.tracks:
                        total = total + session.total_listening_seconds()
            total_minutes = total /60
            list_of_artists.append((artist,total_minutes))
        list_of_artists.sort(key=lambda x: x[1], reverse= True)
        return list_of_artists[:n]



    def user_top_genre(self, user_id):
        user = self.get_user(user_id)

        if user is None:
            return None
        if len(user.sessions) == 0:
            return None

        total = 0
        listening_per_genre = {}

        for session in user.sessions:
            genre = session.track.genre
            listening_time = session.duration_listened_seconds
            total = total + listening_time

            if genre not in listening_per_genre:
                listening_per_genre[genre] = 0
            listening_per_genre[genre] = listening_per_genre[genre] + listening_time

        best = None
        max_time = 0

        for genre in listening_per_genre:
            if listening_per_genre[genre] > max_time:
                max_time = listening_per_genre[genre]
                best = genre
        percentage = (max_time / total) *100
        return (best, percentage)


    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        colab_playlists = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artists.add(track.artist)
                if len(artists) > threshold:
                    colab_playlists.append(playlist)
        return colab_playlists


    def avg_tracks_per_playlist_type(self):
        count_playlists =0
        playlist_tracks = 0
        count_colaborative_playlist = 0
        colaborative_playlists_tracks =0


        for playlist in self._playlists.values():
            if isinstance(playlist, Playlist):
                if not isinstance(playlist, CollaborativePlaylist):
                    count_playlists = count_playlists + 1
                    playlist_tracks = playlist_tracks + len(playlist.tracks)
                elif isinstance(playlist, CollaborativePlaylist):
                    count_colaborative_playlist = count_colaborative_playlist + 1
                    colaborative_playlists_tracks = colaborative_playlists_tracks + len(playlist.tracks)

        if count_playlists == 0:
            avrage_play = 0.0
        else:
            avrage_play =  playlist_tracks/ count_playlists

        if count_colaborative_playlist ==0:
            avrage_collab =0.0
        else:
            avrage_collab = colaborative_playlists_tracks/count_colaborative_playlist

        return {"Playlist":avrage_play, "CollaborativePlaylist": avrage_collab }



    def users_who_completed_albums(self):
        users_who_completed_albums = []
        for user in self._users.values():
            albums_completed = []
            for album in self._albums.values():
                all_tracks = True
                for track in album.tracks:
                    found = False

                    for session in user.sessions:
                        if session.track == track:
                            found = True

                    if found == False:
                        all_tracks = False

                if all_tracks == True:
                    albums_completed.append(album.title)
            if len(albums_completed) >0:
                users_who_completed_albums.append((user, albums_completed))
        return users_who_completed_albums


