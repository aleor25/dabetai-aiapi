import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.services.database import Base
import app.api.deps as deps
from app.main import app


@pytest.fixture(scope='function')
def test_db():
    """Create a fresh in-memory database for each test with all tables created"""
    # Use in-memory SQLite with StaticPool to keep connection alive during test
    TEST_DATABASE_URL = "sqlite:///:memory:"
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    
    # Create all tables in the test database BEFORE creating session
    Base.metadata.create_all(bind=test_engine)
    
    # Create sessionmaker for test engine
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        expire_on_commit=False
    )
    
    # Create and yield a single session for the test
    session = TestingSessionLocal()
    
    yield session
    
    # Clean up
    session.close()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture()
def client(test_db):
    """Create a test client with isolated in-memory database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass  # Don't close - let the fixture handle it

    # Override the dependency in FastAPI app
    app.dependency_overrides[deps.get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # Clean up overrides
    app.dependency_overrides.clear()
