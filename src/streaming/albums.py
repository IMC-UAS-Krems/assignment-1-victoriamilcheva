class Album:
    """Represents an ordered collection of album tracks."""

    def __init__(self, album_id: str, title: str, release_year: int) -> None:
        self.album_id = album_id
        self.title = title
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track) -> None:
        """Add an AlbumTrack, set its album, and keep the list sorted."""
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number)

    @property
    def track_ids(self) -> list[str]:
        """Return the ordered list of track ids."""
        ids = []
        for track in self.tracks:
            ids.append(track.track_id)
        return ids

    @property
    def duration_seconds(self) -> int:
        """Return the total duration of all tracks in seconds."""
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total
