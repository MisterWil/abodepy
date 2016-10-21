import argparse
import time

from abode import AbodeController

parser = argparse.ArgumentParser()

parser.add_argument('--username', help='Username', required=True)
parser.add_argument('--password', help='Password', required=True)
parser.add_argument('--mode', help='Alarm Mode', required=False)
parser.add_argument('--devices', help='List All Devices',
                    required=False, default=False, action="store_true")
parser.add_argument('--device', help='Get Device', required=False, action='append')
parser.add_argument('--listen', help='Listen For Device Updates',
                    required=False, default=False, action="store_true")
parser.add_argument('--debug', help='Output Debugging',
                    required=False, default=False, action="store_true")

args = vars(parser.parse_args())

if args['mode'] is not None:
    args['mode'] = args['mode'].lower()
    if args['mode'] not in ('standby', 'away', 'home'):
        sys.exit("State must be one of 'standby', 'away', or 'home'.")

a = AbodeController(args['username'], args['password'], args['debug'])

'''if args['mode'] is not None:
    print("Mode set to: %s" % a.set_mode(args['mode']))
else:
    print("System mode: %s" % a.get_mode())'''

'''if args['devices']:
    print(a.get_devices())'''

def _device_callback(device):
    print("Device Callback: %s %s" % (device.name, device.get_value('status')))

if args['device']:
    for device_id in args['device']:
        device = a.get_device(device_id)

        if device:
            print("Device Name: %s, Device Type: %s, Device Status: %s" % (device.get_value('name'), device.get_value('type'), device.get_value('status')))

            a.register(device, _device_callback)
        else:
            print("Could not find device with id: %s" % device_id)

if args['listen']:
    print("Listening for device updates...")
    a.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        a.stop()
        print("Device update listening stopped.")
        pass

a.logout()
