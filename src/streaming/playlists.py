class Playlist:
    """A normal user playlist with ordered unique tracks."""

    def __init__(self, playlist_id: str, title: str, owner) -> None:
        self.playlist_id = playlist_id
        self.title = title
        self.owner = owner
        self.tracks = []

    def add_track(self, track) -> None:
        """Add a track only once."""
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track) -> None:
        """Remove a track if it exists."""
        if track in self.tracks:
            self.tracks.remove(track)

    @property
    def total_duration_seconds(self) -> int:
        """Return the total playlist duration in seconds."""
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    """A playlist that can have multiple contributors."""

    def __init__(self, playlist_id: str, title: str, owner) -> None:
        super().__init__(playlist_id, title, owner)
        self.contributors = [owner]

    def add_contributor(self, user) -> None:
        """Add a contributor if not already present."""
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user) -> None:
        """Remove a contributor, but never remove the owner."""
        if user == self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)