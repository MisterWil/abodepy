python-abode
=============================================
A thin Python library for the Abode alarm API.
Only compatible with Python 3+

Disclaimer:
~~~~~~~~~~~~~~~
Published under the MIT license - See LICENSE file for more details.

"Abode" is a trademark owned by Abode Systems Inc., see www.goabode.com for more information.
I am in no way affiliated with Abode.

Thank you Abode for having a relatively simple API to reverse engineer. Hopefully in the future you'll
open it up for official use.

API calls faster than 60 seconds is not recommended as it can overwhelm Abode's servers. Leverage the cloud push
event notification functionality as much as possible. Please use this module responsibly.

Installation
============
Standalone from source::

    pip3 install .

From PyPi:

    pip3 install abodepy
  
Command Line Usage
==================
Simple command line implementation arguments::

    $ python abodecl.py
        usage: abodecl.py --username USERNAME --password PASSWORD
                        [--mode] [--arm ARM] [--devices] [--device DEVICE] [--listen] [--debug]
                        
You can get the current alarm mode::

    $ python abodecl.py --username USERNAME --password PASSWORD --mode
    
    Mode: standby
    
To set the alarm mode, one of 'standby', 'home', or 'away'::

    $ python abodecl.py --username USERNAME --password PASSWORD --arm home
    
    Mode set to: home

A full list of devices and their current states::

    $ python abodecl.py --username USERNAME --password PASSWORD --devices
    
    Device Name: Glass Break Sensor, Device ID: RF:xxxxxxxx, Device Type: GLASS, Device Status: Online
    Device Name: Keypad, Device ID: RF:xxxxxxxx, Device Type: Keypad, Device Status: Online
    Device Name: Remote, Device ID: RF:xxxxxxxx, Device Type: Remote Controller, Device Status: Online
    Device Name: Garage Entry Door, Device ID: RF:xxxxxxxx, Device Type: Door Contact, Device Status: Closed
    Device Name: Front Door, Device ID: RF:xxxxxxxx, Device Type: Door Contact, Device Status: Closed
    Device Name: Back Door, Device ID: RF:xxxxxxxx, Device Type: Door Contact, Device Status: Closed
    Device Name: Status Indicator, Device ID: ZB:xxxxxxxx, Device Type: Status Display, Device Status: Online
    Device Name: Downstairs Motion Camera, Device ID: ZB:xxxxxxxx, Device Type: Motion Camera, Device Status: Online
    Device Name: Back Door Deadbolt, Device ID: ZW:xxxxxxxx, Device Type: Door Lock, Device Status: LockClosed
    Device Name: Front Door Deadbolt, Device ID: ZW:xxxxxxxx, Device Type: Door Lock, Device Status: LockClosed
    Device Name: Garage Door Deadbolt, Device ID: ZW:xxxxxxxx, Device Type: Door Lock, Device Status: LockClosed
    Device Name: Alarm area_1, Device ID: area_1, Device Type: Alarm, Device Status: standby

The current state of a specific device using the device id::

    $ python abodecl.py --username USERNAME --password PASSWORD --device ZW:xxxxxxxx
    
    Device Name: Garage Door Deadbolt, Device ID: ZW:xxxxxxxx, Device Type: Door Lock, Device Status: LockClosed

Additionally, multiple specific devices using the device id::
    
    $ python abodecl.py --username USERNAME --password PASSWORD --device ZW:xxxxxxxx --device RF:xxxxxxxx
    
    Device Name: Garage Door Deadbolt, Device ID: ZW:xxxxxxxx, Device Type: Door Lock, Device Status: LockClosed
    Device Name: Back Door, Device ID: RF:xxxxxxxx, Device Type: Door Contact, Device Status: Closed
   
You can also block and listen for all device change events::

    $ python abodecl.py --username USERNAME --password PASSWORD --listen
    
        No devices specified, adding all devices to listener...
        Listening for device updates...
        Device Name: Alarm area_1, Device ID: area_1, Status: standby, At: 2017-05-27 11:13:08
        Device Name: Garage Door Deadbolt, Device ID: ZW:xxxxxxxx, Status: LockOpen, At: 2017-05-27 11:13:31
        Device Name: Garage Entry Door, Device ID: RF:xxxxxxxx, Status: Open, At: 2017-05-27 11:13:34
        Device Name: Garage Entry Door, Device ID: RF:xxxxxxxx, Status: Closed, At: 2017-05-27 11:13:39
        Device Name: Garage Door Deadbolt, Device ID: ZW:xxxxxxxx, Status: LockClosed, At: 2017-05-27 11:13:41
        Device Name: Alarm area_1, Device ID: area_1, Status: home, At: 2017-05-27 11:13:59
        Device update listening stopped.
        
If you specify one or more devices with the --device argument along with the --listen command then only those devices will listen for change events.

Keyboard interupt CTRL+C to exit listening mode.

Testing
=======

To test from source directly, run pytest with the PWD added to the python path::

    $ python -m pytest tests

Library Usage
=============
TODO

Class Descriptions
==================
TODO