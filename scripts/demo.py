import httpx
import json
from random import randrange

host = "http://127.0.0.1:8000"

# List all users
print("Listing all existing users")
users = httpx.get(f"{host}/users").json()
print(json.dumps(users, indent=2))

input()


# Create new user bad request
print("Create user with missing field, expect a validation error")
body = {"username": "foo", "first_name": "foo", "last_name": "bar"}
response = httpx.post(f"{host}/users", json=body)
print(response.status_code)
print(json.dumps(response.json(), indent=2))

input()

print("Trying to get user with non UUID string will also cause a validation error")
response = httpx.get(f"{host}/users/bad-id")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

input()

print("Now create a new user")
body["email"] = "foo.bar@example.com"
user_id = httpx.post(f"{host}/users", json=body).json()["id"]

scores = [randrange(0, 100) for _ in range(5)]
print(f"Adding scores {scores} for new user {user_id}")
for score in scores:
    httpx.post(
        f"{host}/scores",
        json={"game": "pro-coding", "score": score, "user_id": user_id},
    )

print(f"listing all scores for user {user_id}")
user_scores = httpx.get(f"{host}/scores", params={"user_id": user_id}).json()
print(json.dumps(user_scores, indent=2))
