class Track:
    """Base class for every playable item on the platform."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
    ) -> None:
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    @property
    def duration_minutes(self) -> float:
        """Return the duration converted from seconds to minutes."""
        return self.duration_seconds / 60

    def __eq__(self, other) -> bool:
        """Two tracks are equal if they have the same id."""
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

    def __hash__(self) -> int:
        """Allow tracks to be used in sets and as dict keys."""
        return hash(self.track_id)


class Song(Track):
    """A music track that belongs to an artist."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist
        self.artist.add_track(self)


class SingleRelease(Song):
    """A song released as a standalone single."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist,
        release_date,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date


class AlbumTrack(Song):
    """A song that is part of an album."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist,
        track_number: int,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = None


class Podcast(Track):
    """A podcast episode with a host and optional description."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        description: str = "",
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class InterviewEpisode(Podcast):
    """A podcast interview episode with a guest."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        guest: str,
        description: str = "",
    ) -> None:
        super().__init__(
            track_id,
            title,
            duration_seconds,
            genre,
            host,
            description,
        )
        self.guest = guest


class NarrativeEpisode(Podcast):
    """A narrative podcast episode with season and episode number."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        season: int,
        episode_number: int,
        description: str = "",
    ) -> None:
        super().__init__(
            track_id,
            title,
            duration_seconds,
            genre,
            host,
            description,
        )
        self.season = season
        self.episode_number = episode_number


class AudiobookTrack(Track):
    """A chapter or section from an audiobook."""

    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        book_title: str,
        author: str,
        chapter_number: int,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.book_title = book_title
        self.author = author
        self.chapter_number = chapter_number