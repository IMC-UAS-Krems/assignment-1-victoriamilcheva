from __future__ import annotations
from datetime import datetime, timedelta
from .albums import Album
from .artists import Artist
from .playlists import CollaborativePlaylist, Playlist
from .sessions import ListeningSession
from .tracks import Song, Track
from .users import FamilyMember, PremiumUser, User


class StreamingPlatform:
    def __init__(self, name: str) -> None:
        self.name = name
        self._catalogue: dict[str, Track] = {}
        self._users: dict[str, User] = {}
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._playlists: dict[str, Playlist] = {}
        self._sessions: list[ListeningSession] = []

    def add_track(self, track: Track) -> None:
        self._catalogue[track.track_id] = track

    def add_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession) -> None:
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str) -> Track | None:
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def get_artist(self, artist_id: str) -> Artist | None:
        return self._artists.get(artist_id)

    def get_album(self, album_id: str) -> Album | None:
        return self._albums.get(album_id)

    def all_users(self) -> list[User]:
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        return list(self._catalogue.values())

    # Q1
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_seconds = 0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0

    # Q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users: list[PremiumUser] = []
        for user in self._users.values():
            if type(user) is PremiumUser:
                premium_users.append(user)

        if len(premium_users) == 0:
            return 0.0

        window_start = datetime.now() - timedelta(days=days)
        total_unique_tracks = 0

        for user in premium_users:
            unique_track_ids: set[str] = set()
            for session in user.sessions:
                if session.timestamp >= window_start:
                    unique_track_ids.add(session.track.track_id)
            total_unique_tracks += len(unique_track_ids)

        return total_unique_tracks / len(premium_users)

    # Q3
    def track_with_most_distinct_listeners(self) -> Track | None:
        if len(self._sessions) == 0:
            return None

        listeners_by_track: dict[str, set[str]] = {}
        for session in self._sessions:
            track_id = session.track.track_id
            if track_id not in listeners_by_track:
                listeners_by_track[track_id] = set()
            listeners_by_track[track_id].add(session.user.user_id)

        best_track: Track | None = None
        best_listener_count = -1

        for track in self._catalogue.values():
            current_count = len(listeners_by_track.get(track.track_id, set()))
            if current_count > best_listener_count:
                best_listener_count = current_count
                best_track = track

        return best_track

    # Q4
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        grouped_durations: dict[str, list[int]] = {}

        for session in self._sessions:
            user_type_name = type(session.user).__name__
            if user_type_name not in grouped_durations:
                grouped_durations[user_type_name] = []
            grouped_durations[user_type_name].append(session.duration_listened_seconds)

        result: list[tuple[str, float]] = []
        for user_type_name, durations in grouped_durations.items():
            average_duration = sum(durations) / len(durations)
            result.append((user_type_name, float(average_duration)))

        result.sort(key=lambda item: item[1], reverse=True)
        return result

    # Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_seconds = 0
        for session in self._sessions:
            current_user = session.user
            if isinstance(current_user, FamilyMember) and current_user.age < age_threshold:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0

    # Q6
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        seconds_by_artist: dict[Artist, float] = {}

        for session in self._sessions:
            current_track = session.track
            if isinstance(current_track, Song):
                current_artist = current_track.artist
                if current_artist not in seconds_by_artist:
                    seconds_by_artist[current_artist] = 0.0
                seconds_by_artist[current_artist] += session.duration_listened_seconds

        ranked_artists = []
        for artist, total_seconds in seconds_by_artist.items():
            ranked_artists.append((artist, total_seconds / 60.0))

        ranked_artists.sort(key=lambda item: item[1], reverse=True)
        return ranked_artists[:n]
    
    def user_top_genre(self, user_id: str):
        return None

    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        return []

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        return {"Playlist": 0.0, "CollaborativePlaylist": 0.0}

    def users_who_completed_albums(self):
        return []
