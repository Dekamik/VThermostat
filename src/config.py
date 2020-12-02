#!/user/bin/env python

commands = {
    "temperatureReadoutCmd": "bash ~/bin/temperature.sh",
    "heaterOnCmd": "bash ~/bin/heater.sh on",
    "heaterOffCmd": "bash ~/bin/heater.sh off",
    "heaterCheckCmd": "bash ~/bin/heater.sh check | awk '{print ($2 == \"ON\")}'",
    "fanOnCmd": "bash ~/bin/fan.sh on",
    "fanOffCmd": "bash ~/bin/fan.sh off",
    "fanCheckCmd": "bash ~/bin/fan.sh check | awk '{print ($2 == \"ON\")}'",
}
