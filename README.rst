python-abode |Build Status| |Coverage Status|
=================================================
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
From PyPi:

    pip3 install abodepy
  
Command Line Usage
==================
Simple command line implementation arguments::

    $ python abodepy.py -h
        usage: abodepy.py [-h] --username USERNAME --password PASSWORD [--mode]
                          [--arm ARM] [--setting SETTING] [--switchOn SWITCHON]
                          [--switchOff SWITCHOFF] [--lock LOCK] [--unlock UNLOCK]
                          [--devices] [--device DEVICE] [--listen] [--debug] [--quiet]
        
        optional arguments:
          -h, --help            show this help message and exit
          --username USERNAME   Username
          --password PASSWORD   Password
          --mode                Output Alarm Mode
          --arm ARM             Arm Alarm To Mode
          --setting SETTING     Set Setting
          --switchOn SWITCHON   Switch On Given Device ID
          --switchOff SWITCHOFF
                                Switch Off Given Device ID
          --lock LOCK           Lock Given Device ID
          --unlock UNLOCK       Unlock Given Device ID
          --devices             List All Devices
          --device DEVICE       Get Device
          --listen              Listen For Device Updates
          --debug               Logging at Debug Level
          --quiet               Output Warn Level

You can get the current alarm mode::

    $ python abodepy.py --username USERNAME --password PASSWORD --mode
    
    Mode: standby
    
To set the alarm mode, one of 'standby', 'home', or 'away'::

    $ python abodepy.py --username USERNAME --password PASSWORD --arm home
    
    Mode set to: home

A full list of devices and their current states::

    $ python abodepy.py --username USERNAME --password PASSWORD --devices
    
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

    $ python abodepy.py --username USERNAME --password PASSWORD --device ZW:xxxxxxxx
    
    Device Name: Garage Door Deadbolt, Device ID: ZW:xxxxxxxx, Device Type: Door Lock, Device Status: LockClosed

Additionally, multiple specific devices using the device id::
    
    $ python abodepy.py --username USERNAME --password PASSWORD --device ZW:xxxxxxxx --device RF:xxxxxxxx
    
    Device Name: Garage Door Deadbolt, Device ID: ZW:xxxxxxxx, Device Type: Door Lock, Device Status: LockClosed
    Device Name: Back Door, Device ID: RF:xxxxxxxx, Device Type: Door Contact, Device Status: Closed
    
You can switch a device on or off, or lock and unlock a device by passing multiple arguments::

    $ python abodepy.py --username USERNAME --password PASSWORD --lock ZW:xxxxxxxx --switchOn ZW:xxxxxxxx
    
    Locked device with id: ZW:xxxxxxxx
    Switched on device with id: ZW:xxxxxxxx
   
You can also block and listen for all mode and change events as they occur::

    $ python abodepy.py --username USERNAME --password PASSWORD --listen
    
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

Keyboard interupt (CTRL+C) to exit listening mode.

Settings
========

You can change settings with abodepy either using abode.set_setting(setting, value) or through the command line::

  $ python abodepy.py --username USERNAME --password PASSWORD --setting beeper_mute=1
  
    Setting beeper_mute changed to 1

+-----------------------+-----------------------------------------------------------------------------+
| Setting               | Valid Values                                                                |
+=======================+=============================================================================+
| ircamera_resolution_t | 0 for 320x240x3, 2 for 640x480x3                                            |
+-----------------------+-----------------------------------------------------------------------------+
| ircamera_gray_t       | 0 for disabled, 1 for enabled                                               |
+-----------------------+-----------------------------------------------------------------------------+
| beeper_mute           | 0 for disabled, 1 for enabled                                               |
+-----------------------+-----------------------------------------------------------------------------+
| away_entry_delay      | 0, 10, 20, 30, 60, 120, 180, 240                                            |
+-----------------------+-----------------------------------------------------------------------------+
| away_exit_delay       | 30, 60, 120, 180, 240                                                       |
+-----------------------+-----------------------------------------------------------------------------+
| home_entry_delay      | 0, 10, 20, 30, 60, 120, 180, 240                                            |
+-----------------------+-----------------------------------------------------------------------------+
| home_exit_delay       | 0, 10, 20, 30, 60, 120, 180, 240                                            |
+-----------------------+-----------------------------------------------------------------------------+
| door_chime            | none, normal, loud                                                          |
+-----------------------+-----------------------------------------------------------------------------+
| warning_beep          | none, normal, loud                                                          |
+-----------------------+-----------------------------------------------------------------------------+
| entry_beep_away       | none, normal, loud                                                          |
+-----------------------+-----------------------------------------------------------------------------+
| exit_beep_away        | none, normal, loud                                                          |
+-----------------------+-----------------------------------------------------------------------------+
| entry_beep_home       | none, normal, loud                                                          |
+-----------------------+-----------------------------------------------------------------------------+
| exit_beep_home        | none, normal, loud                                                          |
+-----------------------+-----------------------------------------------------------------------------+
| confirm_snd           | none, normal, loud                                                          |
+-----------------------+-----------------------------------------------------------------------------+
| alarm_len             | 0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900 |
+-----------------------+-----------------------------------------------------------------------------+
| final_beep            | 0, 3, 4, 5, 6, 7, 8, 9, 10                                                  |
+-----------------------+-----------------------------------------------------------------------------+



Development and Testing
=======================

Install the core dependencies::

    $ sudo apt-get install python3-pip python3-dev python3-venv

Checkout from github and then create a virtual environment::

    $ git clone https://github.com/MisterWil/abodepy.git
    $ cd abodepy
    $ python3 -m venv venv
    
Activate the virtual environment::

    $ source venv/bin/activate
    
Install abodepy locally::

    $ pip3 install .

To test from source directly, run pytest with the PWD added to the python path::

    $ python -m pytest tests
    
Alternatively you can run the run the full test suite with tox::

    $ tox

Library Usage
=============
TODO

Class Descriptions
==================
TODO

.. |Build Status| image:: https://travis-ci.org/MisterWil/abodepy.svg?branch=master
    :target: https://travis-ci.org/MisterWil/abodepy
.. |Coverage Status| image:: https://coveralls.io/repos/github/MisterWil/abodepy/badge.svg
    :target: https://coveralls.io/github/MisterWil/abodepy
