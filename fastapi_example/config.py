import os
import dotenv
from typing import Annotated
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class Config(BaseModel):
    db_file: Annotated[
        str,
        Field(
            default_factory=lambda: os.getenv("DB_FILE") or "fastapi_example.db.json"
        ),
    ]


config = Config.model_validate({})
