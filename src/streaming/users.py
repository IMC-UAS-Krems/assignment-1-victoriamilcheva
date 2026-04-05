from __future__ import annotations
from abc import ABC
from datetime import date
class User(ABC):
    def __init__(self, user_id: str, name: str, age: int) -> None:
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions: list = []

    def add_session(self, session) -> None:
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        total = 0
        for session in self.sessions:
            total += session.duration_listened_seconds
        return total

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self) -> set[str]:
        track_ids: set[str] = set()
        for session in self.sessions:
            track_ids.add(session.track.track_id)
        return track_ids

    def __str__(self) -> str:
        return self.name


class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6

    def __init__(self, user_id: str, name: str, age: int) -> None:
        super().__init__(user_id, name, age)


class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date) -> None:
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(User):
    def __init__(self, user_id: str, name: str, age: int) -> None:
        super().__init__(user_id, name, age)
        self.sub_users: list[FamilyMember] = []

    def add_sub_user(self, sub_user) -> None:
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)

    def all_members(self) -> list[User]:
        members: list[User] = [self]
        for sub_user in self.sub_users:
            members.append(sub_user)
        return members


class FamilyMember(User):
    def __init__(self, user_id: str, name: str, age: int, parent: FamilyAccountUser) -> None:
        super().__init__(user_id, name, age)
        self.parent = parent
        if self not in parent.sub_users:
            parent.add_sub_user(self)
