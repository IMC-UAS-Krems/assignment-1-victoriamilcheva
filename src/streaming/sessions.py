class ListeningSession:
    """stores one listening event of a user"""
    def __init__(
        self,
        session_id: str,
        user,
        track,
        timestamp,
        duration_seconds: int
    ) -> None:
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_seconds = duration_seconds
        self.duration_listened_seconds = duration_seconds

    def duration_listened_minutes(self) -> float:
        return self.duration_seconds / 60