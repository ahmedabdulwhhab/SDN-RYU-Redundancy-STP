#python 3

# sudo mn --controller=remote,ip=192.168.1.12 --switch=ovsk,protocols=OpenFlow13 --topo=single,4 --mac

#curl -X GET http://127.0.0.1:8080/simpleswitch/mactable/0000000000000001

import requests
import json

ip_address= '127.0.0.1'
port = '8080'
rest_path = '/simpleswitch/mactable'
switch = '0000000000000001'
pad = 20


url = 'http://{}:{}{}/{}'.format(ip_address, port, rest_path, switch)

response = requests.get(url)
response_bytes = response.content
response_str = response_bytes.decode('utf-8')

if (response.ok):
	json_dict = json.loads(response_str)
else:
	print('there has been a problem connecting to REST API')
	exit(1)

#print equivalent 'curl' command
heading = 'Equivalent cURL command to interact with server from serve'
print('\n{}'.format(heading))
print('-' * len(heading), '\n')

print(' $ crul {}'.format(url))

#print out the naked list received
heading = ' Naked JSON list received from server'
print('\n{}'.format(heading))
print('-' * len(heading), '\n')

print(json_dict)

#Breaddown list into individual element pairs
heading = ' Breaddown list into individual element pairs received from server'
print('\n{}'.format(heading))
print('-' * len(heading), '\n')

print('MAC address {} port'.format(' '*7))
print('{} {} {}'.format('-' * 11,' '*7, '-'*4))
print()

for mac in sorted(json_dict.keys()):
    pad_digits = pad - len(mac)
    print('{} {} {}'.format(mac,' ' * pad_digits, json_dict[mac]))
    
#END
exit(0)
