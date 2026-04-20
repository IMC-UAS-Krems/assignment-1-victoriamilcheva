class Playlist:
    """user playlist with ordered tracks"""
    def __init__(self, playlist_id: str, title: str, owner) -> None:
        self.playlist_id = playlist_id
        self.title = title
        self.owner = owner
        self.tracks = []

    def add_track(self, track) -> None:
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_or_id) -> None:
        if isinstance(track_or_id, str):
            for track in self.tracks:
                if track.track_id == track_or_id:
                    self.tracks.remove(track)
                    return
        else:
            if track_or_id in self.tracks:
                self.tracks.remove(track_or_id)

    def total_duration_seconds(self) -> int:
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, title: str, owner) -> None:
        super().__init__(playlist_id, title, owner)
        self.contributors = [owner]

    def add_contributor(self, user) -> None:
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user) -> None:
        if user == self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)