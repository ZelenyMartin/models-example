import random
from contextlib import asynccontextmanager
from pathlib import Path

import yaml
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.data = []

    for f in Path("data").glob("*.yaml"):
        app.state.data.extend(yaml.safe_load(f.read_text(encoding="utf-8")))

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> dict:
    return random.choice(app.state.data)
