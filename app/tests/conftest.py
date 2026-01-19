import pytest
import os
import tempfile
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    
    SQLALCHEMY_TEST_DATABASE_URL = f"sqlite:///{db_path}"
    
    # Create test engine
    engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Create the products table directly
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(120) NOT NULL,
                sku VARCHAR(50) UNIQUE NOT NULL,
                price FLOAT NOT NULL,
                active BOOLEAN DEFAULT 1
            )
        """))
        conn.commit()
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Patch database module BEFORE importing app
    import sys
    import app.storage.database as db_module
    
    # Save originals
    original_engine = db_module.engine
    original_sessionlocal = db_module.SessionLocal
    original_url = db_module.SQLALCHEMY_DATABASE_URL
    
    # Replace with test versions
    db_module.SQLALCHEMY_DATABASE_URL = SQLALCHEMY_TEST_DATABASE_URL
    db_module.engine = engine
    db_module.SessionLocal = TestingSessionLocal
    
    # Flush any cached modules
    for key in list(sys.modules.keys()):
        if key.startswith('app.routers') or key == 'app.main':
            del sys.modules[key]
    
    # Now import the app
    from app.main import app
    
    # Override get_db
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    from app.gateway.routers.products import get_db
    app.dependency_overrides[get_db] = override_get_db
    
    # Create and yield client
    client = TestClient(app)
    yield client
    
    # Cleanup
    app.dependency_overrides.clear()
    
    # Restore originals
    db_module.SQLALCHEMY_DATABASE_URL = original_url
    db_module.engine = original_engine
    db_module.SessionLocal = original_sessionlocal
    
    # Remove temp database
    try:
        os.remove(db_path)
    except:
        pass
