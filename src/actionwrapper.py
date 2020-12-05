import configparser
import logging
import subprocess

from enum import Enum


class DeviceStatus(Enum):
    OFF = 0
    ON = 1


class ActionWrapper:
    def __init__(self, config: configparser.ConfigParser):
        self.config = config

    def read_temperature(self):
        logging.debug("read_temperature")
        try:
            temperature = float(subprocess.run(self.config.get("commands", "temperatureReadoutCmd"),
                                               shell=True, stdout=subprocess.PIPE).stdout)
            logging.debug("OK (" + str(temperature) + ")")
            return temperature
        except ValueError:
            logging.error("temperatureReadoutCmd output not valid. Expecting number.")
            raise

    def heater_status(self):
        logging.debug("heater_status")
        try:
            status = bool(subprocess.run(self.config.get("commands", "heaterCheckCmd"),
                                         shell=True, stdout=subprocess.PIPE).stdout)
            logging.debug("OK")
            return status
        except ValueError:
            logging.error("heaterCheckCmd output not valid. Expecting boolean value.")
            raise

    def heater(self, new_status: DeviceStatus):
        logging.debug("heater")
        if new_status == DeviceStatus.OFF:
            try:
                subprocess.run(self.config.get("commands", "heaterOffCmd"), shell=True)
            except ValueError:
                logging.error("heaterOffCmd not valid.")
                raise
        elif new_status == DeviceStatus.ON:
            try:
                subprocess.run(self.config.get("commands", "heaterOnCmd"), shell=True)
            except ValueError:
                logging.error("heaterOnCmd not valid.")
                raise
        logging.debug("OK")

    def fan_status(self):
        logging.debug("fan_status")
        try:
            status = bool(subprocess.run(self.config.get("commands", "fanCheckCmd"),
                                         shell=True, stdout=subprocess.PIPE).stdout)
            logging.debug("OK")
            return status
        except ValueError:
            logging.error("fanCheckCmd output not valid. Expecting boolean value.")
            raise

    def fan(self, new_status: DeviceStatus):
        logging.debug("fan")
        if new_status == DeviceStatus.OFF:
            try:
                subprocess.run(self.config.get("commands", "fanOffCmd"), shell=True)
            except ValueError:
                logging.error("fanOffCmd not valid.")
                raise
        elif new_status == DeviceStatus.ON:
            try:
                subprocess.run(self.config.get("commands", "fanOnCmd"), shell=True)
            except ValueError:
                logging.error("fanOnCmd not valid.")
                raise
        logging.debug("OK")
