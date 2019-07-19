from main import app, database, get_db
from starlette.testclient import TestClient
import pytest
import asyncio
from databases import Database

database = Database("sqlite:///./test_test.db", force_rollback=True)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def db():
    return database


@pytest.fixture
def client():
    database = Database("sqlite:///./test_test.db", force_rollback=True)
    app.dependency_overrides[get_db] = db
    with TestClient(app) as client:
        yield client
        app.dependency_overrides = {}


def test_create_notes(client: TestClient):
    r = client.post("/notes/", json={"text": "bullshit", "completed": True})
    assert r.status_code == 200
    assert r.json()["id"] is not None
    assert r.json()["text"] == "bullshit"
    assert r.json()["completed"]


def test_list_notes(client: TestClient):
    r = client.get("/notes/")
    assert r.status_code == 200
    assert len(r.json()) == 0
