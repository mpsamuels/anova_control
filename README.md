# Anova_controller.py
A Python CLI wrapper for the [pyanova-api](https://github.com/ammarzuberi/pyanova-api) module to interface with the [Anova](https://anovaculinary.com/) private API used by the [Anova Precision Cooker Pro](https://anovaculinary.com/anova-precision-cooker/pro/). Particularly intended for integrating an [Anova Precision Cooker Pro](https://anovaculinary.com/anova-precision-cooker/pro/) with [Home Assistant](https://www.home-assistant.io/).

This may work with other [Anova](https://anovaculinary.com/) cookers but has only been tested with the [Anova Precision Cooker Pro](https://anovaculinary.com/anova-precision-cooker/pro/).

# Acknowledgements
This wouldn't have been possible without:

[danodemano's](https://github.com/danodemano/) [anova_control.py](https://github.com/danodemano/anova.py/blob/master/anova_control.py) script which works with older Anova cooker models and provided a starting point plus a lot of the inspiration for this CLI wrapper

[ammarzuberi's](https://github.com/ammarzuberi/) [pyanova-api](https://github.com/ammarzuberi/pyanova-api) Python module which this wrapper relies on to operate.

# How to use it

## Prerequisites
[pyanova-api](https://github.com/ammarzuberi/pyanova-api) must be installed for this script to work:

### Install pyanova-api Python module

#### Quick install
From the command line, run
```pip install pyanova-api```

#### Manual install
- Clone the GitHub repository:
```git clone https://github.com/ammarzuberi/pyanova-api.git```
- Enter the newly created `pyanova-api` directory and run:
```pip install .```

#### Home Assistant Docker container install
If running [Home Assistant](https://www.home-assistant.io/) within a [Docker](https://www.docker.com/) container, the above installation methods will see the [pyanova-api](https://github.com/ammarzuberi/pyanova-api) module removed on each reboot or upgrade of the container.

To ensure the installation persists:

- First, add the [hassio addons development](https://github.com/home-assistant/hassio-addons-development) repo to your HA installation
- Install the 'Custom deps deployment' add-on
- In the add-on configuration, add '- pyanova-api' under the 'pypi' heading
```
pypi:
  - pyanova-api
```
- Save the configuration
- Start the add-on
- Ensure the add-on is set to start on boot.

### Find your cooker_id
You can find your cooker's device ID from the [Anova](https://anovaculinary.com/) mobile phone app:

Profile > Settings cog > Cooker Details

### Obtain authentication credentials
The [pyanova-api](https://github.com/ammarzuberi/pyanova-api) can not authenticate using Google, Facebook or Apple authentication tokens, you must sign up to anovaculincary.io by e-mail and connect the Anova Cooker to this account for this script to function as expected.

## Installation
Once all pre-requisites are met, clone this repository or copy anova_control.py to the machine that has [pyanova-api](https://github.com/ammarzuberi/pyanova-api) installed.

If using Home Assistant, cloning this repo into the \config\scripts folder is recommended or copy anova_control.py to  \config\scripts\anova_control\anova_control.py.

## Script usage
anova_control.py requires the following arguments to run:

-o/--output [r/j/raw/json] Set whether the output is presented as a raw text string or in JSON format. JSON is recommended for Home Assistant integration

-i/--id/--cooker_id [Anova Device ID] 

-u/--username/-e/--email [email address used to login to anovaculinary.io account]

-p/--password [password used to login to anovaculinary.io account]

This will output the full suite of information available from [pyanova-api](https://github.com/ammarzuberi/pyanova-api) in the format requested, plain text or JSON.

## Use with Home Assistant
### Command line sensor
Create a [Home Assistant command line sensor](https://www.home-assistant.io/integrations/sensor.command_line/) to pull the JSON output into [Home Assistant](https://www.home-assistant.io/) as the entity 'sensor.anova_status':
```
platform: command_line
command: 'python ./scripts/anova_control/anova_control.py -o j -i <cooker ID> -u <username> -p <password>'
name: Anova Status
json_attributes:
    - job_status
    - job_time_remaining
    - heater_duty_cycle
    - motor_duty_cycle
    - wifi_connected
    - wifi_ssid
    - water_leak
    - water_level_low
    - water_level_critical
    - heater_temp
    - triac_temp
    - water_temp
value_template: '{{value_json.current_temp}}'
scan_interval: 1
```
While the Anova cooker is not powered on, the status will be reported as 'unknown' in Home Assistant and only the 'friendly_name: Anova Status' attribute will be reported. Once the device is powered on, all attributes should be visible.

### Template Sensors
The following template sensors pull the individual values from the command line sensor to read each value as a specific entity:
```
platform: template
sensors:
  anova_job_status:
    friendly_name: 'Anova job status'
    value_template:
        '{{ states.sensor.anova_status.attributes.job_status }}'
  anova_job_time_remaining:
    friendly_name: 'Anova job time remaining'
    unit_of_measurement: 'min'
    value_template:
        '{{ states.sensor.anova_status.attributes.job_time_remaining/60 | round(0) }}'
  anova_heater_duty_cycle:
    friendly_name: 'Anova heater duty cycle'
    unit_of_measurement: '°C'
    value_template: 
        '{{ states.sensor.anova_status.attributes.heater_duty_cycle }}'
  anova_motor_duty_cycle:
    friendly_name: 'Anova motor duty cycle'
    unit_of_measurement: '°C'
    value_template: 
        '{{ states.sensor.anova_status.attributes.motor_duty_cycle }}'
  anova_wifi_connected:
    friendly_name: 'Anova wifi connected'
    value_template: 
        '{{ states.sensor.anova_status.attributes.wifi_connected }}'
  anova_wifi_ssid:
    friendly_name: 'Anova wifi ssid'
    value_template: 
        '{{ states.sensor.anova_status.attributes.wifi_ssid }}'
  anova_water_leak:
    friendly_name: 'Anova water leak'
    value_template: 
        '{{ states.sensor.anova_status.attributes.water_leak }}'
  anova_water_level_low:
    friendly_name: 'Anova water level low'
    value_template: 
        '{{ states.sensor.anova_status.attributes.water_level_low }}'
  anova_water_level_critical:
    friendly_name: 'Anova water level critical'
    value_template: 
        '{{ states.sensor.anova_status.attributes.water_level_critical }}'
  anova_heater_temp:
    friendly_name: 'Anova heater_temp'
    unit_of_measurement: '°C'
    value_template: 
        '{{ states.sensor.anova_status.attributes.heater_temp }}'
  anova_triac_temp:
    friendly_name: 'Anova triac temp'
    unit_of_measurement: '°C'
    value_template: 
        '{{ states.sensor.anova_status.attributes.triac_temp }}'
  anova_water_temp:
    friendly_name: 'Anova water temp'
    unit_of_measurement: '°C'
    value_template: 
        '{{ states.sensor.anova_status.attributes.water_temp }}'
```

# To Do
Implement Start/Edit/Stop cook functionality to allow the cooker to be controlled from HA. This script currently only reads info from the device and reports on it.

Document other potential sensors to allow better integration into HA.