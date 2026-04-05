"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

class User:
    def __init__(self,user_id: str, name: str, age: int, sessions = None):
        self.user_id = user_id
        self.name = name
        self.age = age

        if sessions is not None:
            self.sessions: list["ListeningSession"] = list(sessions)
        else:
            self.sessions= []

    def add_session(self,session:"ListeningSession"):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total =0
        for session in self.sessions:
            total += session.duration_listened_seconds
        return total

    def total_listening_minutes(self):
        return self.total_listening_seconds()/60

    def unique_tracks_listened(self):
        track_ids = set()
        for session in self.sessions:
            track_ids.add(session.track.track_id)
        return track_ids




class FamilyAccountUser(User):
    def __init__(self,user_id: str, name: str, age: int,  sub_users = None, sessions= None):
        super().__init__(user_id, name, age, sessions)
        if sub_users is not None:
            self.sub_users: list["FamilyMember"] = list(sub_users)
        else:
            self.sub_users= []

    def add_sub_user(self, sub_user: "FamilyMember") -> None:
        self.sub_users.append(sub_user)

    def all_members(self) -> list[User]:
        return [self] + self.sub_users


class FreeUser(User):
    MAX_SKIPS_PER_HOUR: int = 6
    def __init__(self,user_id: str, name: str, age: int, sessions = None):
        super().__init__(user_id, name, age, sessions)


class PremiumUser(User):
    def __init__(self,user_id: str, name: str, age: int,  subscription_start: date,sessions = None,):
        super().__init__(user_id, name, age, sessions)
        self.subscription_start = subscription_start

class FamilyMember(User):
    def __init__(self,user_id: str, name: str, age: int, parent,  sessions = None):
        super().__init__(user_id, name, age, sessions)
        self.parent = parent


