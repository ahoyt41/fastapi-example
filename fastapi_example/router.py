from typing import Annotated, Optional
from uuid import UUID

from pydantic import NonNegativeInt
from starlette.types import AppType
from fastapi_example.models import (
    FullScore,
    NewScoreRequest,
    NewUserRequest,
    UpdateUserRequest,
    User,
)
from fastapi import APIRouter, Depends, HTTPException, Query

from fastapi_example.service import MockService
from fastapi_example.dependencies import svc_dep

user_router = APIRouter(prefix="/users", tags=["Users"])
score_router = APIRouter(prefix="/scores", tags=["Scores"])


Service = Annotated[MockService, Depends(svc_dep)]


@user_router.get("")
async def list_users(svc: Service) -> list[User]:
    """
    list all of the available users. The svc variable is passed
    in using a FastAPI class based dependency
    """
    return await svc.list_users()


@user_router.get("/{user_id}")
async def get_user(svc: Service, user_id: UUID) -> User:
    """
    Get a user by their ID, the user_id is parsed from the URL.
    All parts of the url wrapped in {} are parsed and are available
    to be used as arguments to the handler function.
    """
    user = await svc.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@user_router.post("", status_code=201)
async def create_user(svc: Service, user: NewUserRequest) -> User:
    """
    The user variable is a subclass of a Pydantic base class. As a result
    FastAPI will interpret the body of the request as JSON and try to parse
    it into an instance of that subclass.
    """
    return await svc.add_user(user)


@user_router.patch("/{user_id}", status_code=202)
async def update_user(svc: Service, user_id: UUID, user: UpdateUserRequest) -> User:
    updated_user = await svc.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return updated_user


@user_router.delete("/{user_id}")
async def delete_user(svc: Service, user_id: UUID) -> None:
    await svc.delete_user(user_id)


@score_router.get("")
async def list_scores(
    svc: Service,
    user_id: Annotated[Optional[UUID], Query()] = None,
    lower_bound: Annotated[NonNegativeInt, Query()] = 0,
    upper_bound: Annotated[NonNegativeInt, Query()] = 100,
) -> list[FullScore]:
    if upper_bound > 100:
        upper_bound = 100
    if upper_bound <= lower_bound:
        raise HTTPException(
            status_code=400, detail="upper bound must be greater than lower bound"
        )
    return await svc.list_scores(user_id, lower_bound, upper_bound)


@score_router.get("/{score_id}")
async def get_score(svc: Service, score_id: UUID) -> FullScore:
    score = await svc.get_score(score_id)
    if score is None:
        raise HTTPException(status_code=404, detail=f"score {score} not found")
    return score


@score_router.post("", status_code=201)
async def create_score(svc: Service, score: NewScoreRequest) -> FullScore:
    try:
        return await svc.add_score(score)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"could not create new score for user {score.user_id}, user does not exist",
        )


@score_router.delete("/{score_id}")
async def delete_score(svc: Service, score_id: UUID) -> None:
    await svc.delete_score(score_id)
