import subprocess

from enum import Enum
from . import config


class DeviceStatus(Enum):
    OFF = 0
    ON = 1


class ActionWrapper:

    @staticmethod
    def read_temperature():
        return float(subprocess.run(config.commands["temperatureReadoutCmd"], shell=True, stdout=subprocess.PIPE).stdout)

    @staticmethod
    def heater_status():
        return bool(subprocess.run(config.commands["heaterCheckCmd"], shell=True, stdout=subprocess.PIPE).stdout)

    @staticmethod
    def heater(new_status: DeviceStatus):
        if new_status == DeviceStatus.OFF:
            subprocess.run(config.commands["heaterOffCmd"], shell=True)
        elif new_status == DeviceStatus.ON:
            subprocess.run(config.commands["heaterOnCmd"], shell=True)

    @staticmethod
    def fan_status():
        return bool(subprocess.run(config.commands["fanCheckCmd"], shell=True, stdout=subprocess.PIPE).stdout)

    @staticmethod
    def fan(new_status: DeviceStatus):
        if new_status == DeviceStatus.OFF:
            subprocess.run(config.commands["fanOffCmd"], shell=True)
        elif new_status == DeviceStatus.ON:
            subprocess.run(config.commands["fanOnCmd"], shell=True)
