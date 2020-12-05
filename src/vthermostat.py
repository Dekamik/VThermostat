#!/user/bin/env python
import logging
import sys

from actionwrapper import ActionWrapper
from actionwrapper import DeviceStatus


class VThermostat:
    def __init__(self, actions: ActionWrapper):
        logging.debug("__init__")
        self.actions = actions

        self.usage = sys.argv[0] + " [--min n] [--max n] [--heater on/off] [--fan on/off] [--help]"

        self.min = None
        self.max = None
        self.turn_heater_on = None
        self.turn_fan_on = None

        self.temperature = None
        self.is_fan_on = False
        self.is_heater_on = False
        logging.debug("OK")

    def parse_args(self, args):
        logging.debug("parse_args...")
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
                logging.critical("Expected a value after " + arg)
                raise

            except ValueError:
                logging.critical("Illegal value " + sys.argv[i + 1] + " for " + arg)
                raise
        logging.debug("OK")

    def read_sensors(self):
        logging.debug("read_sensors...")
        try:
            self.temperature = self.actions.read_temperature()
        except ValueError:
            logging.critical("Could not read temperature. Check if temperatureReadoutCmd is valid in app.conf.")
        try:
            self.is_heater_on = self.actions.heater_status()
        except ValueError:
            logging.critical("Could not read fan status. Check if fanCheckCmd is valid in app.conf.")
        try:
            self.is_fan_on = self.actions.fan_status()
        except ValueError:
            logging.critical("Could not read heater status. Check if heaterChecmCmd is valid in app.conf.")
        logging.debug("OK")

    def validate(self):
        logging.debug("validate...")
        if (self.min is None and self.max is not None) or (self.min is not None and self.max is None):
            raise ValueError("Both min and max must be defined if used.")

        if self.min > self.max:
            raise ValueError("min cannot be larger than max.")
        logging.debug("OK")

    def check_temperature(self):
        logging.debug("check_temperature...")
        logging.info("TEMPERATURE : " + self.temperature + "°C")
        logging.info("HEATER      : " + "ON" if self.is_heater_on else "OFF")
        logging.info("FAN         : " + "ON" if self.is_fan_on else "OFF")

        if self.min is not None and self.max is not None:
            if self.temperature < self.min and not self.is_heater_on:
                self.turn_heater_on = True
                if self.is_fan_on:
                    self.turn_fan_on = False

            elif self.temperature > self.max and not self.is_fan_on:
                self.turn_fan_on = True
                if self.is_heater_on:
                    self.turn_heater_on = False

        logging.info("Heater should be " + "ON" if self.turn_heater_on else "OFF")
        logging.info("Fan should be " + "ON" if self.turn_fan_on else "OFF")
        logging.debug("OK")

    def do_actions(self):
        logging.debug("do_actions...")
        # Heater
        if self.turn_heater_on is not None:
            if not self.is_heater_on and self.turn_heater_on:
                self.actions.heater(DeviceStatus.ON)
                logging.info("Heater turned ON")

            elif self.is_heater_on and not self.turn_heater_on:
                self.actions.heater(DeviceStatus.OFF)
                logging.info("Heater turned OFF")

        # Fan
        if self.turn_fan_on is not None:
            if not self.is_fan_on and self.turn_fan_on:
                self.actions.fan(DeviceStatus.ON)
                logging.info("Fan turned ON")

            elif self.is_fan_on and not self.turn_fan_on:
                self.actions.fan(DeviceStatus.OFF)
                logging.info("Fan turned OFF")

        logging.debug("OK")


if __name__ == "__main__":
    thermostat = VThermostat(ActionWrapper())

    thermostat.parse_args(sys.argv)
    thermostat.read_sensors()
    thermostat.validate()
    thermostat.check_temperature()
    thermostat.do_actions()
