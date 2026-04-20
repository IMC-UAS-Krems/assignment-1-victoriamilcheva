class Artist:
    """Represents a music artist or content creator."""

    def __init__(self, artist_id: str, name: str) -> None:
        self.artist_id = artist_id
        self.name = name
        self.tracks = []

    @property
    def track_count(self) -> int:
        """Return how many tracks are linked to this artist."""
        return len(self.tracks)

    def add_track(self, track) -> None:
        """Add a track to the artist if it is not already present."""
        if track not in self.tracks:
            self.tracks.append(track)
