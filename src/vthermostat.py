#!/user/bin/env python
import sys

from .actionwrapper import ActionWrapper
from .actionwrapper import DeviceStatus


class VThermostat:
    def __init__(self, actions: ActionWrapper):
        self.actions = actions

        self.usage = sys.argv[0] + " [--min n] [--max n] [--heater on/off] [--fan on/off] [--help]"

        self.min = None
        self.max = None
        self.turn_heater_on = None
        self.turn_fan_on = None

        self.temperature = None
        self.is_fan_on = False
        self.is_heater_on = False

    def parse_args(self, args):
        for i, arg in enumerate(args):
            try:
                if arg == "--min":
                    self.min = float(args[i + 1])

                elif arg == "--max":
                    self.max = float(args[i + 1])

                elif arg == "--heater":
                    self.turn_heater_on = args[i + 1] == "on"

                elif arg == "--fan":
                    self.turn_fan_on = args[i + 1] == "on"

                elif arg == "--help" or len(args) == 1:
                    print(self.usage)
                    exit(0)

            except IndexError:
                print("Expected a value after " + arg)
                raise

            except ValueError:
                print("Illegal value " + sys.argv[i + 1] + " for " + arg)
                raise

    def parse_readouts(self):
        self.temperature = self.actions.read_temperature()
        self.is_heater_on = self.actions.heater_status()
        self.is_fan_on = self.actions.fan_status()

    def validate(self):
        if (self.min is None and self.max is not None) or (self.min is not None and self.max is None):
            raise ValueError("Both min and max must be defined if used.")

        if self.min > self.max:
            raise ValueError("min cannot be larger than max.")

    def check_temperature(self):
        if self.min is not None and self.max is not None:
            if self.temperature < self.min and not self.is_heater_on:
                self.turn_heater_on = True
                if self.is_fan_on:
                    self.turn_fan_on = False

            elif self.temperature > self.max and not self.is_fan_on:
                self.turn_fan_on = True
                if self.is_heater_on:
                    self.turn_heater_on = False

    def do_actions(self):
        # Heater
        if self.turn_heater_on is not None:
            if not self.is_heater_on and self.turn_heater_on:
                self.actions.heater(DeviceStatus.ON)
            elif self.is_heater_on and not self.turn_heater_on:
                self.actions.heater(DeviceStatus.OFF)

        # Fan
        if self.turn_fan_on is not None:
            if not self.is_fan_on and self.turn_fan_on:
                self.actions.fan(DeviceStatus.ON)
            elif self.is_fan_on and not self.turn_fan_on:
                self.actions.fan(DeviceStatus.OFF)


if __name__ == "__main__":
    thermostat = VThermostat(ActionWrapper())

    thermostat.parse_args(sys.argv)
    thermostat.parse_readouts()
    thermostat.validate()
    thermostat.check_temperature()
    thermostat.do_actions()
