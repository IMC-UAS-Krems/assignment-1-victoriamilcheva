class User:
    def __init__(self, user_id: str, name: str, age: int) -> None:
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session) -> None:
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        total = 0
        for session in self.sessions:
            total += session.duration_seconds
        return total

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self) -> set[str]:
        track_ids = set()
        for session in self.sessions:
            track_ids.add(session.track.track_id)
        return track_ids


class FreeUser(User):
    pass


class PremiumUser(User):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        subscription_start=None
    ) -> None:
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        subscription_start=None
    ) -> None:
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users = []

    def add_member(self, member) -> None:
        if member not in self.sub_users:
            self.sub_users.append(member)

    def add_sub_user(self, member) -> None:
        self.add_member(member)

    def all_members(self) -> list:
        return [self] + list(self.sub_users)


class FamilyMember(User):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        parent
    ) -> None:
        super().__init__(user_id, name, age)
        self.parent = parent
        self.parent_account = parent
        self.parent.add_member(self)