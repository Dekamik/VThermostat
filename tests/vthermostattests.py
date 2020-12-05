#!/user/bin/env python
import unittest
from unittest.mock import MagicMock

from src.vthermostat import VThermostat
from src.actionwrapper import DeviceStatus


class VThermostatTests(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.actions = MagicMock()
        self.thermostat = VThermostat(self.actions, self.logger)

    def test_parse_args__min__min_set(self):
        self.thermostat.parse_args(["--min", "1"])
        self.assertEqual(1, self.thermostat.min)

    def test_parse_args__max__max_set(self):
        self.thermostat.parse_args(["--max", "1"])
        self.assertEqual(1, self.thermostat.max)

    def test_parse_args__heater_on__heater_on_true(self):
        self.thermostat.parse_args(["--heater", "on"])
        self.assertEqual(True, self.thermostat.turn_heater_on)

    def test_parse_args__heater_off__heater_on_false(self):
        self.thermostat.parse_args(["--heater", "off"])
        self.assertEqual(False, self.thermostat.turn_heater_on)

    def test_parse_args__fan_on__fan_on_true(self):
        self.thermostat.parse_args(["--fan", "on"])
        self.assertEqual(True, self.thermostat.turn_fan_on)

    def test_parse_args__fan_off__fan_on_false(self):
        self.thermostat.parse_args(["--fan", "off"])
        self.assertEqual(False, self.thermostat.turn_fan_on)

    def test_read_sensors__any_condition__readout_methods_called(self):
        self.thermostat.read_sensors()
        self.actions.read_temperature.assert_called_once()
        self.actions.heater_status.assert_called_once()
        self.actions.fan_status.assert_called_once()

    def test_validate__only_min_set__ValueError_raised(self):
        self.thermostat.min = 1
        with self.assertRaises(ValueError):
            self.thermostat.validate()

    def test_validate__only_max_set__ValueError_raised(self):
        self.thermostat.max = 1
        with self.assertRaises(ValueError):
            self.thermostat.validate()

    def test_validate__min_larger_than_max__ValueError_raised(self):
        self.thermostat.max = -1
        self.thermostat.min = 1
        with self.assertRaises(ValueError):
            self.thermostat.validate()

    def test_check_temperature__too_cold_is_heater_on_false__heater_on_true(self):
        self.thermostat.temperature = 17
        self.thermostat.min = 19
        self.thermostat.max = 22
        self.thermostat.is_heater_on = False
        self.thermostat.check_temperature()
        self.assertEqual(True, self.thermostat.turn_heater_on)

    def test_check_temperature__too_warm_is_heater_on_true__heater_on_true(self):
        self.thermostat.temperature = 23
        self.thermostat.min = 19
        self.thermostat.max = 22
        self.thermostat.is_heater_on = True
        self.thermostat.check_temperature()
        self.assertEqual(False, self.thermostat.turn_heater_on)

    def test_do_actions__heater_to_be_turned_on__heater_turned_on(self):
        self.thermostat.is_heater_on = False
        self.thermostat.turn_heater_on = True
        self.thermostat.do_actions()
        self.actions.heater.assert_called_once_with(DeviceStatus.ON)

    def test_do_actions__heater_to_be_turned_off__heater_turned_off(self):
        self.thermostat.is_heater_on = True
        self.thermostat.turn_heater_on = False
        self.thermostat.do_actions()
        self.actions.heater.assert_called_once_with(DeviceStatus.OFF)

    def test_do_actions__fan_to_be_turned_on__fan_turned_on(self):
        self.thermostat.is_fan_on = False
        self.thermostat.turn_fan_on = True
        self.thermostat.do_actions()
        self.actions.fan.assert_called_once_with(DeviceStatus.ON)

    def test_do_actions__fan_to_be_turned_off__fan_turned_off(self):
        self.thermostat.is_fan_on = True
        self.thermostat.turn_fan_on = False
        self.thermostat.do_actions()
        self.actions.fan.assert_called_once_with(DeviceStatus.OFF)


if __name__ == '__main__':
    unittest.main()
