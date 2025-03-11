from src.main.domain import (
    Promotion, PromotionId, Teacher, TeacherId, Course, CourseId, Room, RoomId,
    PlanningSlot, PlanningSlotId
)


class TestPromotion:
    """Test cases for Promotion class."""
    def test_given_study_year_and_diploma_and_name_when_create_promotion_then_return_promotion(self):
        # Given
        promotion_id = PromotionId(id="1")
        study_year = 2
        diploma = "DEUST"
        name = "Kempf"
        # When
        promotion = Promotion(id=promotion_id, study_year=study_year, diploma=diploma, name=name)
        # Then
        assert promotion.study_year == study_year
        assert promotion.diploma == diploma
        assert promotion.name == name


class TestTeacher:
    """Test cases for Teacher class."""
    def test_given_name_and_firstname_when_create_teacher_then_return_teacher(self):
        # Given
        teacher_id = TeacherId(id="1")
        name = "Doe"
        firstname = "John"
        # When
        teacher = Teacher(id=teacher_id, name=name, firstname=firstname)
        # Then
        assert teacher.name == name
        assert teacher.firstname == firstname


class TestCourse:
    """Test cases for Course class."""
    def test_given_name_when_create_course_then_return_course(self):
        # Given
        course_id = CourseId(id="1")
        name = "Mathematics"
        # When
        course = Course(id=course_id, name=name)
        # Then
        assert course.name == name


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


class TestPlanningSlot:
    """Test cases for PlanningSlot class."""
    def test_given_valid_times_and_entities_when_create_planning_slot_then_return_planning_slot(self):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 9
        minutes_start = 0
        hours_end = 10
        minutes_end = 0
        promotion = Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf")
        teacher = Teacher(id=TeacherId(id="1"), name="Doe", firstname="John")
        course = Course(id=CourseId(id="1"), name="Mathematics")
        room = Room(id=RoomId(id="1"), name="Room 101", description="First floor room")
        # When
        planning_slot = PlanningSlot(
            id=planning_slot_id,
            hours_start=hours_start,
            minutes_start=minutes_start,
            hours_end=hours_end,
            minutes_end=minutes_end,
            promotion=promotion,
            teacher=teacher,
            course=course,
            room=room
        )
        # Then
        assert planning_slot.hours_start == hours_start
        assert planning_slot.minutes_start == minutes_start
        assert planning_slot.hours_end == hours_end
        assert planning_slot.minutes_end == minutes_end
        assert planning_slot.promotion == promotion
        assert planning_slot.teacher == teacher
        assert planning_slot.course == course
        assert planning_slot.room == room

    def test_given_invalid_end_time_when_create_planning_slot_then_raise_value_error(self):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 10
        minutes_start = 0
        hours_end = 9
        minutes_end = 0
        promotion = Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf")
        teacher = Teacher(id=TeacherId(id="1"), name="Doe", firstname="John")
        course = Course(id=CourseId(id="1"), name="Mathematics")
        room = Room(id=RoomId(id="1"), name="Room 101", description="First floor room")
        # When/Then
        try:
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                promotion=promotion,
                teacher=teacher,
                course=course,
                room=room
            )
        except ValueError as e:
            assert 'End time must be after start time' in str(e)

    def test_given_invalid_duration_when_create_planning_slot_then_raise_value_error(self):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 9
        minutes_start = 0
        hours_end = 9
        minutes_end = 15
        promotion = Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf")
        teacher = Teacher(id=TeacherId(id="1"), name="Doe", firstname="John")
        course = Course(id=CourseId(id="1"), name="Mathematics")
        room = Room(id=RoomId(id="1"), name="Room 101", description="First floor room")
        # When/Then
        try:
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                promotion=promotion,
                teacher=teacher,
                course=course,
                room=room
            )
        except ValueError as e:
            assert 'Slot duration must be at least 30 minutes' in str(e)

    def test_given_duration_exceeds_four_hours_when_create_planning_slot_then_raise_value_error(self):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 9
        minutes_start = 0
        hours_end = 13
        minutes_end = 1
        promotion = Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf")
        teacher = Teacher(id=TeacherId(id="1"), name="Doe", firstname="John")
        course = Course(id=CourseId(id="1"), name="Mathematics")
        room = Room(id=RoomId(id="1"), name="Room 101", description="First floor room")
        # When/Then
        try:
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                promotion=promotion,
                teacher=teacher,
                course=course,
                room=room
            )
        except ValueError as e:
            assert 'Slot duration must be at most 4 hours' in str(e)

    def test_given_invalid_start_time_when_create_planning_slot_then_raise_value_error(self):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 8
        minutes_start = 0
        hours_end = 9
        minutes_end = 0
        promotion = Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf")
        teacher = Teacher(id=TeacherId(id="1"), name="Doe", firstname="John")
        course = Course(id=CourseId(id="1"), name="Mathematics")
        room = Room(id=RoomId(id="1"), name="Room 101", description="First floor room")
        # When/Then
        try:
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                promotion=promotion,
                teacher=teacher,
                course=course,
                room=room
            )
        except ValueError as e:
            assert 'First slot can only start at 08:15 or later' in str(e)

    def test_given_invalid_end_time_limit_when_create_planning_slot_then_raise_value_error(self):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 16
        minutes_start = 0
        hours_end = 17
        minutes_end = 30
        promotion = Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf")
        teacher = Teacher(id=TeacherId(id="1"), name="Doe", firstname="John")
        course = Course(id=CourseId(id="1"), name="Mathematics")
        room = Room(id=RoomId(id="1"), name="Room 101", description="First floor room")
        # When/Then
        try:
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                promotion=promotion,
                teacher=teacher,
                course=course,
                room=room
            )
        except ValueError as e:
            assert 'Last slot can only end at 17:15 or earlier' in str(e)
