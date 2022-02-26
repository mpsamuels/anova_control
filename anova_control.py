#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append( '/config/deps/lib/python3.9/site-packages/anova/' )
import AnovaCooker
import argparse
import json

#Check arguments function
def check_arg(args=None):
	#Set up command line arguments
    parser = argparse.ArgumentParser(description='Script to control Anova cooker. For use with pyanova-api (https://github.com/ammarzuberi/pyanova-api)')
    parser.add_argument('-o', '--output',
						type=str,
                        help='Output type, text string or JSON.',
						choices=['r', 'j', 'raw', 'json'],)
    parser.add_argument('-i', '--id', '--cooker_id',
						type=str,
                        help='Cooker ID, taken from Anova App.')
    parser.add_argument('-u', '--username', '-e', '--email',
						type=str,
                        help='email address to authenticate Anova account.',)
    parser.add_argument('-p', '--password',
						type=str,
                        help='Password to authenticate Anova account.',)	
    results = parser.parse_args(args)
    return (results.output, 
			results.id,
			results.username,
			results.password)
			
if __name__ == '__main__':
	if check_arg(sys.argv[1:]) is not None :
		#Connect to Anova, authenticate and collect cooker status
		o, i, u, p = check_arg(sys.argv[1:])
		cooker = AnovaCooker.AnovaCooker(i)
		cooker.authenticate(u, p)
		cooker.update_state
		if (o == "r") or (o == "raw") :
			#Return cooker status values in raw text from
			print('job_status = ', (cooker.job_status), ', job_time_remaining = ', (cooker.job_time_remaining), ', heater_duty_cycle = ', (cooker.heater_duty_cycle), \
			', motor_duty_cycle = ', (cooker.motor_duty_cycle), ', wifi_connected = ', (cooker.wifi_connected), ', wifi_ssid = ', (cooker.wifi_ssid), ', water_leak = ', (cooker.water_leak), \
			', water_level_low = ', (cooker.water_level_low), ', water_level_critical = ', (cooker.water_level_critical), ', heater_temp = ', (cooker.heater_temp), ', triac_temp = ', (cooker.triac_temp), \
			', water_temp = ', (cooker.water_temp))
		elif (o == "j") or (o == "json") :
			#Build JSON array
			data = {}
			data['job_status'] = cooker.job_status
			data['job_time_remaining'] = cooker.job_time_remaining
			data['heater_duty_cycle'] = cooker.heater_duty_cycle
			data['motor_duty_cycle'] = cooker.motor_duty_cycle
			data['wifi_connected'] = cooker.wifi_connected
			data['wifi_ssid'] = cooker.wifi_ssid
			data['water_leak'] = cooker.water_leak
			data['water_level_low'] = cooker.water_level_low
			data['water_level_critical'] = cooker.water_level_critical
			data['heater_temp'] = cooker.heater_temp
			data['triac_temp'] = cooker.triac_temp
			data['water_temp'] = cooker.water_temp
			json_data = json.dumps(data)
			
			#Output the JSON
			print(json_data)
	else:
		parser=argparse.ArgumentParser('Script to control Anova cooker. For use with pyanova-api (https://github.com/ammarzuberi/pyanova-api)')
		parser.print_help(sys.stderr)