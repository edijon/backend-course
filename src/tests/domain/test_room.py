from src.main.domain.room import Room, RoomId


class TestRoom:
    """Test cases for Room class."""
    def test_given_name_and_description_when_create_room_then_return_room(self):
        # Given
        room_id = RoomId(id="1")
        name = "Room 101"
        description = "First floor room"
        # When
        room = Room(id=room_id, name=name, description=description)
        # Then
        assert room.name == name
        assert room.description == description
