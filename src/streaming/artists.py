"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""
class Artist:
    def __init__(self, artist_id: str, name: str, genre: str, tracks = None):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

        if tracks is not None:
            for track in tracks:
                self.add_track(track)

    def add_track(self, track):
        self.tracks.append(track)

    def track_count(self) -> int:
        return len(self.tracks)
