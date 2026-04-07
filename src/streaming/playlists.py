from __future__ import annotations


class Playlist:
    def __init__(self, playlist_id: str, name: str, owner) -> None:
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: list = []

    def add_track(self, track) -> None:
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_or_id) -> None:
        track_id = track_or_id
        if hasattr(track_or_id, 'track_id'):
            track_id = track_or_id.track_id

        new_tracks = []
        for track in self.tracks:
            if track.track_id != track_id:
                new_tracks.append(track)
        self.tracks = new_tracks

    def total_duration_seconds(self) -> int:
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, owner) -> None:
        super().__init__(playlist_id, name, owner)
        self.contributors: list = [owner]

    def add_contributor(self, user) -> None:
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user) -> None:
        if user == self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)
