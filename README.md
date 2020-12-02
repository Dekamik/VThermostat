# VThermostat

IoT thermostat using TP-Link.

Command is to be run at regular intervals using cron.

When run, it will read the room temperature and check if it is between the pre-defined min-max temperatures. If the temperature is above the max, it will turn on the fan and turn off the heater. If the temperature is below the min, it will instead turn on the heater and turn off the fan.