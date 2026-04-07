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

    #q1
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        all_seconds = 0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                all_seconds += session.duration_listened_seconds
        return all_seconds / 60.0

    #q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = []
        for user in self._users.values():
            if type(user) is PremiumUser:
                premium_users.append(user)
        if len(premium_users) == 0:
            return 0.0
        start_time = datetime.now() - timedelta(days=days)
        total_unique = 0
        for user in premium_users:
            listened_ids = set()
            for session in user.sessions:
                if session.timestamp >= start_time:
                    listened_ids.add(session.track.track_id)
            total_unique += len(listened_ids)
        return total_unique / len(premium_users)

    #q3
    def track_with_most_distinct_listeners(self) -> Track | None:
        if len(self._sessions) == 0:
            return None
        listeners_per_track = {}
        for session in self._sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id
            if track_id not in listeners_per_track:
                listeners_per_track[track_id] = set()
            listeners_per_track[track_id].add(user_id)
        best_track = None
        best_count = -1

        for track in self._catalogue.values():
            current_count = len(listeners_per_track.get(track.track_id, set()))
            if current_count > best_count:
                best_count = current_count
                best_track = track
        return best_track

    #q4
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        seconds_by_type = {}
        for session in self._sessions:
            type_name = type(session.user).__name__
            if type_name not in seconds_by_type:
                seconds_by_type[type_name] = []
            seconds_by_type[type_name].append(session.duration_listened_seconds)
        answer = []
        for type_name, values in seconds_by_type.items():
            average = sum(values) / len(values)
            answer.append((type_name, float(average)))
        answer.sort(key=lambda item: item[1], reverse=True)
        return answer

    #q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        all_seconds = 0
        for session in self._sessions:
            user = session.user
            if isinstance(user, FamilyMember) and user.age < age_threshold:
                all_seconds += session.duration_listened_seconds
        return all_seconds / 60.0

    #q6
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        seconds_per_artist = {}

        for session in self._sessions:
            track = session.track

            if isinstance(track, Song):
                artist = track.artist

                if artist not in seconds_per_artist:
                    seconds_per_artist[artist] = 0
                seconds_per_artist[artist] += session.duration_listened_seconds

        answer = []

        for artist, seconds in seconds_per_artist.items():
            answer.append((artist, seconds / 60.0))

        answer.sort(key=lambda item: item[1], reverse=True)
        return answer[:n]

    #q7
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        user = self.get_user(user_id)
        if user is None:
            return None
        if len(user.sessions) == 0:
            return None
        seconds_per_genre = {}
        all_seconds = 0
        for session in user.sessions:
            genre = session.track.genre
            seconds = session.duration_listened_seconds
            if genre not in seconds_per_genre:
                seconds_per_genre[genre] = 0
            seconds_per_genre[genre] += seconds
            all_seconds += seconds

        best_genre = ""
        best_seconds = -1

        for genre, seconds in seconds_per_genre.items():
            if seconds > best_seconds:
                best_seconds = seconds
                best_genre = genre
        percentage = (best_seconds / all_seconds) * 100.0
        return (best_genre, percentage)

    #q8
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        answer = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artist_ids = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artist_ids.add(track.artist.artist_id)
                if len(artist_ids) > threshold:
                    answer.append(playlist)
        return answer

    #q9
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        normal_counts = []
        collaborative_counts = []
        for playlist in self._playlists.values():
            if type(playlist) is Playlist:
                normal_counts.append(len(playlist.tracks))
            elif isinstance(playlist, CollaborativePlaylist):
                collaborative_counts.append(len(playlist.tracks))
        normal_average = 0.0
        if len(normal_counts) > 0:
            normal_average = sum(normal_counts) / len(normal_counts)
        collaborative_average = 0.0
        if len(collaborative_counts) > 0:
            collaborative_average = sum(collaborative_counts) / len(collaborative_counts)
        return {
            "Playlist": float(normal_average),
            "CollaborativePlaylist": float(collaborative_average),
        }

    #q10
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        answer = []
        for user in self._users.values():
            listened_ids = set()
            for session in user.sessions:
                listened_ids.add(session.track.track_id)
            completed_titles = []
            for album in self._albums.values():
                if len(album.tracks) == 0:
                    continue
                completed = True
                for track in album.tracks:
                    if track.track_id not in listened_ids:
                        completed = False
                        break
                if completed:
                    completed_titles.append(album.title)
            if len(completed_titles) > 0:
                answer.append((user, completed_titles))
        return answer
