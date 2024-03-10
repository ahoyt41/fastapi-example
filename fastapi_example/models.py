from typing import Annotated, Optional
import uuid
from pydantic import UUID4, BaseModel, EmailStr, Field, NonNegativeInt


class User(BaseModel):
    id: Annotated[UUID4, Field(default_factory=uuid.uuid4)]
    username: str
    first_name: str
    last_name: str
    email: EmailStr


class NewUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr


class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class ScoreEntry(BaseModel):
    id: Annotated[UUID4, Field(default_factory=uuid.uuid4)]
    game: str
    score: int
    user_id: UUID4


class NewScoreRequest(BaseModel):
    game: str = "Meatball surgery"  # the name of the game
    score: Annotated[
        NonNegativeInt, Field(lt=101)
    ]  # The score value, which must be 0 <= score <= 100
    user_id: UUID4  # The ID of the user who got this score


class FullScore(BaseModel):
    id: Annotated[UUID4, Field(default_factory=uuid.uuid4)]
    game: str
    score: int
    user: User
