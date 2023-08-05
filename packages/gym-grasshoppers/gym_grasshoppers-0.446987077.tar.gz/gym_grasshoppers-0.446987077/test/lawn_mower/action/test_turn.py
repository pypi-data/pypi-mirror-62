from unittest import TestCase
from gym_grasshoppers.exception.invalid_action_exception import InvalidActionException
from gym_grasshoppers.garden.garden import Garden
from gym_grasshoppers.lawn_mower.action.turn import Turn
from gym_grasshoppers.lawn_mower.lawn_mower import LawnMower


class TestTurn(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        valid_geojson_json = open('../../../resources/valid_geojson.json')
        valid_geojson_string = valid_geojson_json.read()
        valid_geojson_json.close()
        garden = Garden(0.3, valid_geojson_string)
        cls._lawn_mower = LawnMower(garden.starting_point.x, garden.starting_point.y, 0., 0.1, 0.5, 50., False)

    def test_missing_angle(self):
        with self.assertRaises(InvalidActionException):
            Turn(self._lawn_mower, None)

    def test_too_low_angle(self):
        with self.assertRaises(InvalidActionException):
            Turn(self._lawn_mower, -181.)

    def test_too_high_angle(self):
        with self.assertRaises(InvalidActionException):
            Turn(self._lawn_mower, 181.)

    def test_execute(self):
        new_angle = 95.
        Turn(self._lawn_mower, new_angle).execute()
        self.assertEqual(self._lawn_mower.angle, new_angle)
