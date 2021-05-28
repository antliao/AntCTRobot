# -*- coding: utf-8 -*-

import json
import argparse
import time
from exchange_base_function import CryptoExchange
from exchange_base_function import AntCTRobot
from send_notice import *

def read_json(fn):
	with open(fn, 'r') as jsf:
		json_obj = json.load(jsf)
	return json_obj

def print_json(json_obj):
	print(json.dumps(json_obj, indent=4))

def process_arg():
	parser = argparse.ArgumentParser()
	parser.add_argument('--conf', '-c', required=True, help='specify the path and name of the config file')
	return parser.parse_args()

def main():
	args = process_arg()
	print("config: ", args.conf)

	conf_fn = args.conf
	conf = read_json(conf_fn)

	# initiate CryptoExchange:
	exchange = CryptoExchange(conf['exchange_id'], conf['api-keys'], conf['api-secret-key'])

	n_agent = alarm_sound()

	# crypto trend Robot from Ant
	CTR = AntCTRobot(exchange, n_agent)
	CTR.set_rule(conf['rules1']['symbol'], conf['rules1']['timeframe'], conf['rules1']['diff'])
	CTR.run()
	
	exit

if __name__ == '__main__':
	main()
