from unittest.mock import patch
import pytest
from flask.testing import FlaskClient
from flask_socketio import SocketIOTestClient

from ..main import socketio, app
from ..api.models import Game
from ..api.routes.games import current_games
from ..ws.socket_events import user_to_room_map, socket_id_to_user_map
from .constants import TEST_EMAIL, TEST_GAME_ID


@pytest.fixture
def flask_client() -> FlaskClient:
    with app.test_client() as client:
        yield client

@pytest.fixture
def socket_client(flask_client: FlaskClient) -> SocketIOTestClient:
    with socketio.test_client(flask_client) as client:
        yield client

def test_disconnect(socket_client: SocketIOTestClient):
    mock_sid = socket_client.eio_sid
    mock_user = TEST_EMAIL
    mock_room = TEST_GAME_ID

    mock_user_to_room_map = {mock_user: mock_room}
    mock_socket_id_to_user_map =  {mock_sid: mock_user}
    mock_user_rooms = {mock_room: [mock_user]}
    mock_current_games = {mock_room: Game(host_email=mock_user)}
    
    assert socket_client.is_connected()

    with patch.dict(user_to_room_map, mock_user_to_room_map, clear=True):
        with patch.dict(socket_id_to_user_map, mock_socket_id_to_user_map, clear=True):
            with patch.dict(current_games, mock_current_games, clear=True):
                socket_client.disconnect()
                
                assert mock_user_rooms.get(mock_room) == None
                assert mock_current_games.get(mock_room) == None
