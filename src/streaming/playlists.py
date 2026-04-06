"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    def __init__(self, playlist_id: str, name:str, owner, tracks = None):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

        if tracks is not None:
            for track in tracks:
                self.add_track(track)

    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track):
        if track in self.tracks:
            self.tracks.remove(track)

    def total_duration_seconds(self):
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self,playlist_id: str, name:str, owner, tracks= None):
        super().__init__(playlist_id, name, owner, tracks)
        self.contributors = [owner]

    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user is self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)