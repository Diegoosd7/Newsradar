import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

os.environ.setdefault("DISABLE_SCHEDULER", "1")

from app.db.models import Base          # Base que tiene todos los modelos registrados
from app.db.database import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_e2e.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.pop(get_db, None)
    test_engine.dispose()
    Base.metadata.drop_all(test_engine)
    try:
        if os.path.exists("test_e2e.db"):
            os.unlink("test_e2e.db")
    except PermissionError:
        pass  # En Windows el archivo puede tardar en liberarse
