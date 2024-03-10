from typing import Optional
from uuid import UUID
import httpx
from pydantic import TypeAdapter
from fastapi_example.models import (
    FullScore,
    NewScoreRequest,
    NewUserRequest,
    UpdateUserRequest,
    User,
)

UserList = TypeAdapter(list[User])
ScoreList = TypeAdapter(list[FullScore])


class ExampleClient(httpx.Client):

    host: str

    def __init__(self, host: str):
        self.host = host
        super().__init__()

    def _users_path(self) -> str:
        return f"{self.host}/users"

    def _user_id_path(self, user_id: UUID) -> str:
        return f"{self._users_path}/{user_id.hex}"

    def _scores_path(self) -> str:
        return f"{self.host}/scores"

    def _scores_id_path(self, score_id: UUID) -> str:
        return f"{self.host}/scores/{score_id.hex}"

    def list_users(self) -> list[User]:
        response = self.get(self._users_path())
        response.raise_for_status()
        return UserList.validate_json(response.json())

    def get_user(self, user_id: UUID) -> User:
        response = self.get(self._user_id_path(user_id))
        response.raise_for_status()
        return User.model_validate(response.json())

    def create_user(self, user: NewUserRequest) -> User:
        response = self.post(self._users_path(), json=user.model_dump())
        response.raise_for_status()
        return User.model_validate(response.json())

    def update_user(self, user_id: UUID, user: UpdateUserRequest) -> User:
        response = self.patch(self._user_id_path(user_id), json=user.model_dump())
        response.raise_for_status()
        return User.model_validate(response.json())

    def delete_user(self, user_id: UUID) -> None:
        response = self.delete(self._user_id_path(user_id))
        response.raise_for_status()

    def list_scores(
        self,
        user_id: Optional[UUID] = None,
        lower_bound: Optional[int] = None,
        upper_bound: Optional[int] = None,
    ) -> list[FullScore]:
        params = {}
        if user_id:
            params["user_id"] = user_id.hex
        if lower_bound is not None:
            params["lower_bound"] = lower_bound
        if upper_bound is not None:
            params["upper_bound"] = upper_bound
        response = self.get(self._scores_path(), params=params)
        response.raise_for_status()
        return ScoreList.validate_python(response.json())

    def get_score(self, score_id: UUID) -> FullScore:
        response = self.get(self._scores_id_path(score_id))
        response.raise_for_status()
        return FullScore.model_validate(response.json())

    def create_score(self, score: NewScoreRequest) -> FullScore:
        response = self.post(self._scores_path(), json=score.model_dump())
        response.raise_for_status()
        return FullScore.model_validate(response.json())

    def delete_score(self, score_id: UUID) -> None:
        response = self.delete(self._scores_id_path(score_id))
        response.raise_for_status()


class ExampleAsyncClient(httpx.AsyncClient):
    host: str

    def __init__(self, host: str):
        self.host = host
        super().__init__()

    def _users_path(self) -> str:
        return f"{self.host}/users"

    def _user_id_path(self, user_id: UUID) -> str:
        return f"{self._users_path}/{user_id.hex}"

    def _scores_path(self) -> str:
        return f"{self.host}/scores"

    def _scores_id_path(self, score_id: UUID) -> str:
        return f"{self.host}/scores/{score_id.hex}"

    async def list_users(self) -> list[User]:
        response = await self.get(self._users_path())
        response.raise_for_status()
        return UserList.validate_json(response.json())

    async def get_user(self, user_id: UUID) -> User:
        response = await self.get(self._user_id_path(user_id))
        response.raise_for_status()
        return User.model_validate(response.json())

    async def create_user(self, user: NewUserRequest) -> User:
        response = await self.post(self._users_path(), json=user.model_dump())
        response.raise_for_status()
        return User.model_validate(response.json())

    async def update_user(self, user_id: UUID, user: UpdateUserRequest) -> User:
        response = await self.patch(self._user_id_path(user_id), json=user.model_dump())
        response.raise_for_status()
        return User.model_validate(response.json())

    async def delete_user(self, user_id: UUID) -> None:
        response = await self.delete(self._user_id_path(user_id))
        response.raise_for_status()

    async def list_scores(
        self,
        user_id: Optional[UUID] = None,
        lower_bound: Optional[int] = None,
        upper_bound: Optional[int] = None,
    ) -> list[FullScore]:
        params = {}
        if user_id:
            params["user_id"] = user_id.hex
        if lower_bound is not None:
            params["lower_bound"] = lower_bound
        if upper_bound is not None:
            params["upper_bound"] = upper_bound
        response = await self.get(self._scores_path(), params=params)
        response.raise_for_status()
        return ScoreList.validate_python(response.json())

    async def get_score(self, score_id: UUID) -> FullScore:
        response = await self.get(self._scores_id_path(score_id))
        response.raise_for_status()
        return FullScore.model_validate(response.json())

    async def create_score(self, score: NewScoreRequest) -> FullScore:
        response = await self.post(self._scores_path(), json=score.model_dump())
        response.raise_for_status()
        return FullScore.model_validate(response.json())

    async def delete_score(self, score_id: UUID) -> None:
        response = await self.delete(self._scores_id_path(score_id))
        response.raise_for_status()
