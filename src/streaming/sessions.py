class ListeningSession:
    """Stores one listening event of a user playing a track."""

    def __init__(self, user, track, duration_seconds: int, timestamp) -> None:
        self.user = user
        self.track = track
        self.duration_seconds = duration_seconds
        self.timestamp = timestamp

    @property
    def duration_listened_minutes(self) -> float:
        """Return listened duration converted to minutes."""
        return self.duration_seconds / 60