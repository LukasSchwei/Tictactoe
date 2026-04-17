from fastapi.testclient import TestClient
from BACKEND_NAME_PLACEHOLDER.api._app import app, get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Tic Tac Toe API"}

def test_create_user():
    response = client.post("/user?username=Alice&password=password123")
    assert response.status_code == 200
    assert response.json() == {"message": "User created", "user_name": "Alice"}
    
    # Try duplicate
    response2 = client.post("/user?username=Alice&password=password123")
    assert response2.status_code == 400

def test_game_flow():
    # Attempt to create game with non-existent players
    resp = client.post("/game?player_x=P1&player_o=P2")
    assert resp.status_code == 400

    # Setup the users
    client.post("/user?username=pX&password=pX")
    client.post("/user?username=pO&password=pO")

    # Create Game
    game_resp = client.post("/game?player_x=pX&player_o=pO")
    assert game_resp.status_code == 200
    game_id = game_resp.json()["game_id"]
    assert game_resp.json()["player_x"] == "pX"
    assert game_resp.json()["status"] == "in_progress"

    # Get Game
    get_resp = client.get(f"/game/{game_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["current_player"] == "pX"

    # Play moves
    move_1 = client.post(f"/game/{game_id}/play/4")
    assert move_1.status_code == 200
    
    # Verify current state
    board_state = client.get(f"/game/{game_id}")
    assert board_state.json()["board"][4] == "X"
    assert board_state.json()["current_player"] == "pO"

    # Invalid moves
    bad_move = client.post(f"/game/{game_id}/play/14")
    assert bad_move.status_code == 400

    taken_move = client.post(f"/game/{game_id}/play/4")
    assert taken_move.status_code == 400


