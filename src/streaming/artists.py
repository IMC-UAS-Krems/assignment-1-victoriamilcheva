class Artist:
    """ represents music artist """
    def __init__(self, artist_id: str, name: str, genre: str) -> None:
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

    def track_count(self) -> int:
        return len(self.tracks)

    def add_track(self, track) -> None:
        if track not in self.tracks:
            self.tracks.append(track)