from random import randint
from uuid import uuid4

from pydantic import UUID4, BaseModel
from fastapi_example.models import User, ScoreEntry

class Database(BaseModel):
    users: dict[UUID4, User]
    scores: dict[UUID4, ScoreEntry]


users = [
    User(
        id=uuid4(),
        first_name="Benjamin",
        last_name="Pierce",
        username="hawkeye",
        email="hawk@example.com",
    ),
    User(
        id=uuid4(),
        first_name="John",
        last_name="McIntyre",
        username="trapper",
        email="trap@example.com"
    ),
    User(
        id=uuid4(),
        first_name="Frank",
        last_name="Burns",
        username="best_surgeon_burns",
        email="frank@example.com"
    )
]

scores = [
]

for user in users:
    for _ in range(5):
        scores.append(ScoreEntry(
            id=uuid4(),
            game="Meatball surgery",
            score=randint(0, 100),
            user_id=user.id
        ))


db = Database(users={u.id: u for u in users}, scores={s.id: s for s in scores})

with open("fastapi_example.db.json", "w") as f:
    f.write(db.model_dump_json(indent=2))
