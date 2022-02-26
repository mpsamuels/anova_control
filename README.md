# Anova_controller.py
A Python CLI wrapper for pyanova-api module (https://github.com/ammarzuberi/pyanova-api) to interface with the Anova private API used by Anova Precision Cooker Pro. Particularly intended for integrating an Anova Cooker Pro with Home Assistant.

This may work with other Anova cookers but has only been tested with the Anova Cooker Pro.

# How to use it

## Prerequisites
pyanova-api (https://github.com/ammarzuberi/pyanova-api) must be installed for this script to work:

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
If running Home Assistant within a Docker container, the above installation methods will see pyanova-api removed on each reboot or upgrade of the container.

To ensure the installation persists:

- First, add the hassio addons development repo (https://github.com/home-assistant/hassio-addons-development) to your HA installation
- Install the 'Custom deps deployment' add-on
- In the add-on configuration, add '- pyanova-api' under the 'pypi' heading
- Save the configuration
- Start the add-on
- Ensure the add-on is set to start on boot.

### Find your cooker_id
You can find your cooker's device ID from the Anova app:

Profile > Settings cog > Cooker Details

### Obtain authentication credentials
The pyanova-api can not authenticate using Google, Facebook or Apple authentication tokens, you must sign up to anovaculincary.io by e-mail and connect the Anova Cooker to this account for this script to function as expected.

## Installation
Once all pre-requisites are met, clone this repository or copy anova_control.py to the machine that has pyanova-api installed.

If using Home Assistant, cloning this repo into the \config\scripts folder is recommended or copy anova_control.py to  \config\scripts\anova_control\anova_control.py.

## Script usage
anova_control.py requires the following arguments to run:

-o/--output [r/j/raw/json] Set whether the output is in raw text string or JSON format. JSON is recommended for Home Assistant integration

-i/--id/--cooker_id [Anova Device ID] 

-u/--username/-e/--email [email address used to login to anovaculinary.io account]

-p/--password [password used to login to anovaculinary.io account]

This will output the full suite of information available from pyanova-api in the format requested, plain text or JSON.

## Use with Home Assistant
Create a command line sensor to pull the JSON output into Home Assistant:
```
platform: command_line
command: ./scripts/anova_control/anova_control.py -o j -i <cooker ID> -u <username> -p <password>
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