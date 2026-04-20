from datetime import timedelta

from .playlists import CollaborativePlaylist, Playlist
from .tracks import Song
from .users import FamilyMember, PremiumUser


class StreamingPlatform:
    def __init__(self, name: str) -> None:
        self.name = name
        self._tracks = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = []
        self._sessions = []

    def add_track(self, track) -> None:
        self._tracks[track.track_id] = track

    def add_user(self, user) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist) -> None:
        self._playlists.append(playlist)

    def record_session(self, session) -> None:
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str):
        return self._tracks.get(track_id)

    def get_user(self, user_id: str):
        return self._users.get(user_id)

    def get_artist(self, artist_id: str):
        return self._artists.get(artist_id)

    def get_album(self, album_id: str):
        return self._albums.get(album_id)

    def all_users(self) -> list:
        return list(self._users.values())

    def all_tracks(self) -> list:
        return list(self._tracks.values())

    def total_listening_time_minutes(self, start, end) -> float:
        total_seconds = 0

        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_seconds

        return total_seconds / 60

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = []

        for user in self._users.values():
            if isinstance(user, PremiumUser):
                premium_users.append(user)

        if len(premium_users) == 0:
            return 0.0

        if len(self._sessions) == 0:
            return 0.0

        latest_time = self._sessions[0].timestamp
        for session in self._sessions:
            if session.timestamp > latest_time:
                latest_time = session.timestamp

        start_time = latest_time - timedelta(days=days)

        total_unique = 0

        for user in premium_users:
            track_ids = set()

            for session in user.sessions:
                if start_time <= session.timestamp <= latest_time:
                    track_ids.add(session.track.track_id)

            total_unique += len(track_ids)

        return total_unique / len(premium_users)

    def track_with_most_distinct_listeners(self):
        if len(self._sessions) == 0:
            return None

        listeners = {}

        for session in self._sessions:
            track_id = session.track.track_id

            if track_id not in listeners:
                listeners[track_id] = {
                    "track": session.track,
                    "users": set()
                }

            listeners[track_id]["users"].add(session.user.user_id)

        best_track = None
        best_count = -1

        for info in listeners.values():
            count = len(info["users"])
            if count > best_count:
                best_count = count
                best_track = info["track"]

        return best_track

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        grouped = {}

        for user in self._users.values():
            type_name = type(user).__name__
            if type_name not in grouped:
                grouped[type_name] = {"sum": 0, "count": 0}

        for session in self._sessions:
            type_name = type(session.user).__name__
            grouped[type_name]["sum"] += session.duration_seconds
            grouped[type_name]["count"] += 1

        result = []

        for type_name, info in grouped.items():
            if info["count"] == 0:
                average = 0.0
            else:
                average = info["sum"] / info["count"]

            result.append((type_name, average))

        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def total_listening_time_underage_sub_users_minutes(
        self,
        age_threshold: int = 18
    ) -> float:
        total_seconds = 0

        for session in self._sessions:
            if isinstance(session.user, FamilyMember):
                if session.user.age < age_threshold:
                    total_seconds += session.duration_seconds

        return total_seconds / 60

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[object, float]]:
        artist_data = {}

        for session in self._sessions:
            track = session.track

            if isinstance(track, Song):
                artist = track.artist

                if artist.artist_id not in artist_data:
                    artist_data[artist.artist_id] = {
                        "artist": artist,
                        "seconds": 0
                    }

                artist_data[artist.artist_id]["seconds"] += session.duration_seconds

        result = []

        for info in artist_data.values():
            result.append((info["artist"], info["seconds"] / 60))

        result.sort(key=lambda x: x[1], reverse=True)
        return result[:n]

    def user_top_genre(self, user_id: str):
        user = self.get_user(user_id)

        if user is None:
            return None

        total_seconds = 0
        genre_data = {}

        for session in user.sessions:
            genre = session.track.genre
            total_seconds += session.duration_seconds

            if genre not in genre_data:
                genre_data[genre] = 0

            genre_data[genre] += session.duration_seconds

        if total_seconds == 0:
            return None

        best_genre = None
        best_seconds = -1

        for genre, seconds in genre_data.items():
            if seconds > best_seconds:
                best_seconds = seconds
                best_genre = genre

        percentage = (best_seconds / total_seconds) * 100
        return (best_genre, percentage)

    def collaborative_playlists_with_many_artists(
        self,
        threshold: int = 3
    ) -> list[CollaborativePlaylist]:
        result = []

        for playlist in self._playlists:
            if isinstance(playlist, CollaborativePlaylist):
                artist_ids = set()

                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artist_ids.add(track.artist.artist_id)

                if len(artist_ids) > threshold:
                    result.append(playlist)

        return result

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        playlist_total = 0
        playlist_count = 0
        collab_total = 0
        collab_count = 0

        for playlist in self._playlists:
            if type(playlist) is Playlist:
                playlist_total += len(playlist.tracks)
                playlist_count += 1
            elif isinstance(playlist, CollaborativePlaylist):
                collab_total += len(playlist.tracks)
                collab_count += 1

        if playlist_count == 0:
            playlist_avg = 0.0
        else:
            playlist_avg = playlist_total / playlist_count

        if collab_count == 0:
            collab_avg = 0.0
        else:
            collab_avg = collab_total / collab_count

        return {
            "Playlist": playlist_avg,
            "CollaborativePlaylist": collab_avg
        }

    def users_who_completed_albums(self) -> list[tuple[object, list[str]]]:
        result = []

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
                result.append((user, completed_titles))

        return result