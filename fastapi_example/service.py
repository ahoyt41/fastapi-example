from typing import Optional
from asyncio import Lock
from functools import wraps
from uuid import UUID, uuid4
from pydantic import UUID4, BaseModel
from fastapi_example.models import (
    FullScore,
    NewScoreRequest,
    NewUserRequest,
    ScoreEntry,
    UpdateUserRequest,
    User,
)


class MockDatabase(BaseModel):
    users: dict[UUID4, User]
    scores: dict[UUID4, ScoreEntry]


_lock = Lock()


def with_lock(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with _lock:
            return await func(*args, **kwargs)

    return wrapper


class MockService:
    db: MockDatabase

    def __init__(self, db_file: str = "fastapi_example.db.json"):
        with open(db_file) as f:
            self.db = MockDatabase.model_validate_json(f.read())
        return

    @with_lock
    async def list_users(self) -> list[User]:
        return list(self.db.users.values())

    @with_lock
    async def add_user(self, new_user: NewUserRequest) -> User:
        user = User(**new_user.model_dump(), id=uuid4())
        self.db.users[user.id] = user
        return user

    @with_lock
    async def update_user(
        self, user_id: UUID, request: UpdateUserRequest
    ) -> Optional[User]:
        user = self.db.users.get(user_id)
        if user is None:
            return None
        if request.username:
            user.username = request.username
        if request.first_name:
            user.first_name = request.first_name
        if request.last_name:
            user.last_name = request.last_name
        if request.email:
            user.email = request.email
        self.db.users[user.id] = user
        return user

    @with_lock
    async def get_user(self, user_id: UUID) -> Optional[User]:
        return self.db.users.get(user_id)

    @with_lock
    async def delete_user(self, user_id: UUID) -> None:
        if user_id in self.db.users:
            del self.db.users[user_id]

    @with_lock
    async def list_scores(
        self,
        user_id: Optional[UUID] = None,
        lower_limit: int = 0,
        upper_limit: int = 100,
    ) -> list[FullScore]:
        filter_func = lambda score: (
            score.score >= lower_limit
            and score.score <= upper_limit
            and (score.user_id == user_id if user_id is not None else True)
        )
        return [
            FullScore(
                **s.model_dump(exclude={"user_id"}), user=self.db.users[s.user_id]
            )
            for s in self.db.scores.values()
            if filter_func(s)
        ]

    @with_lock
    async def add_score(
        self,
        new_score: NewScoreRequest,
    ) -> FullScore:
        score = ScoreEntry(**new_score.model_dump(), id=uuid4())
        self.db.scores[score.id] = score
        return FullScore(**new_score.model_dump(), user=self.db.users[score.user_id])

    @with_lock
    async def get_score(self, score_id: UUID) -> Optional[FullScore]:
        score = self.db.scores.get(score_id)
        if score is None:
            return None
        user = self.db.users[score.user_id]
        return FullScore(**score.model_dump(exclude={"user_id"}), user=user)

    @with_lock
    async def delete_score(self, score_id: UUID) -> None:
        if score_id in self.db.scores:
            del self.db.scores[score_id]
