from __future__ import annotations
class Playlist:
    def __init__(self, playlist_id: str, name: str, owner) -> None:
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: list = []

    def add_track(self, track) -> None:
        self.tracks.append(track)

    def remove_track(self, track_id: str) -> None:
        self.tracks = [track for track in self.tracks if track.track_id != track_id]

    def total_duration_seconds(self) -> int:
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, owner) -> None:
        super().__init__(playlist_id, name, owner)
        self.contributors: list = []

    def add_contributor(self, user) -> None:
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user) -> None:
        if user in self.contributors:
            self.contributors.remove(user)
