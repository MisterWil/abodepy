"""
Mock devices that mimic actual device data from Abode servers.

This file should be updated any time the Abode server responses
change so we can make sure abodepy can still communicate.
"""

import helpers.constants as const

GLASS_BREAK_DEVICE_ID = 'RF:00000001'


def glass_break_device(devid=GLASS_BREAK_DEVICE_ID, status=const.STATUS_ONLINE,
                       low_battery=False, no_response=False,
                       out_of_order=False, tampered=False):
    """Glass break configurable device mock response."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.glass",
          "type":"GLASS",
          "name":"Glass Break Sensor",
          "area":"1",
          "zone":"6",
          "sort_order":null,
          "is_window":"",
          "bypass":"0",
          "schar_24hr":"0",
          "sresp_mode_0":"0",
          "sresp_entry_0":"0",
          "sresp_exit_0":"0",
          "sresp_mode_1":"5",
          "sresp_entry_1":"5",
          "sresp_exit_1":"0",
          "sresp_mode_2":"5",
          "sresp_entry_2":"5",
          "sresp_exit_2":"0",
          "sresp_mode_3":"5",
          "sresp_entry_3":"5",
          "sresp_exit_3":"0",
          "version":"",
          "origin":"abode",
          "control_url":"",
          "deep_link":null,
          "status_color":"#5cb85c",
          "faults":{
             "low_battery":''' + str(int(low_battery)) + ''',
             "tempered":''' + str(int(tampered)) + ''',
             "supervision":0,
             "out_of_order":''' + str(int(out_of_order)) + ''',
             "no_response":''' + str(int(no_response)) + '''
          },
          "status":"''' + status + '''",
          "statuses":{
             "hvac_mode":null
          },
          "status_ex":"",
          "actions":[
          ],
          "status_icons":[
          ],
          "icon":"assets/icons/unknown.svg"
       }'''


KEYPAD_DEVICE_ID = 'RF:00000002'


def keypad_device(devid=KEYPAD_DEVICE_ID, status=const.STATUS_ONLINE,
                  low_battery=False, no_response=False):
    """Key pad configurable device mock response."""
    return '''
       {
          "id":"''' + devid + '''",
          "type_tag":"device_type.keypad",
          "type":"Keypad",
          "name":"Keypad",
          "area":"1",
          "zone":"10",
          "sort_order":null,
          "is_window":"",
          "bypass":"0",
          "schar_24hr":"0",
          "sresp_mode_0":"5",
          "sresp_entry_0":"5",
          "sresp_exit_0":"5",
          "sresp_mode_1":"5",
          "sresp_entry_1":"5",
          "sresp_exit_1":"5",
          "sresp_mode_2":"5",
          "sresp_entry_2":"5",
          "sresp_exit_2":"5",
          "sresp_mode_3":"5",
          "sresp_entry_3":"5",
          "sresp_exit_3":"5",
          "version":"",
          "origin":"abode",
          "control_url":"",
          "deep_link":null,
          "status_color":"#5cb85c",
          "faults":{
             "low_battery":''' + str(int(low_battery)) + ''',
             "tempered":0,
             "supervision":0,
             "out_of_order":0,
             "no_response":''' + str(int(no_response)) + '''
          },
          "status":"''' + status + '''",
          "statuses":{
             "hvac_mode":null
          },
          "status_ex":"",
          "actions":[
          ],
          "status_icons":[
          ],
          "icon":"assets/icons/keypad-b.svg"
       }'''


DOOR_CONTACT_DEVICE_ID = 'RF:00000003'


def door_contact_device(devid=DOOR_CONTACT_DEVICE_ID,
                        status=const.STATUS_CLOSED,
                        low_battery=False, no_response=False):
    """Door contact configurable device mock response."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.door_contact",
          "type":"Door Contact",
          "name":"Back Door",
          "area":"1",
          "zone":"2",
          "sort_order":null,
          "is_window":"",
          "bypass":"0",
          "schar_24hr":"0",
          "sresp_mode_0":"3",
          "sresp_entry_0":"3",
          "sresp_exit_0":"0",
          "sresp_mode_1":"1",
          "sresp_entry_1":"1",
          "sresp_exit_1":"0",
          "sresp_mode_2":"1",
          "sresp_entry_2":"1",
          "sresp_exit_2":"0",
          "sresp_mode_3":"1",
          "sresp_entry_3":"1",
          "sresp_exit_3":"0",
          "version":"",
          "origin":"abode",
          "control_url":"",
          "deep_link":null,
          "status_color":"#5cb85c",
          "faults":{
             "low_battery":''' + str(int(low_battery)) + ''',
             "tempered":0,
             "supervision":0,
             "out_of_order":0,
             "no_response":''' + str(int(no_response)) + '''
          },
          "status":"''' + status + '''",
          "statuses":{
             "hvac_mode":null
          },
          "status_ex":"",
          "actions":[
          ],
          "status_icons":{
             "Open":"assets/icons/door-open-red.svg",
             "Closed":"assets/icons/door-closed-green.svg"
          },
          "sresp_trigger":"0",
          "sresp_restore":"0",
          "icon":"assets/icons/doorsensor-a.svg"
       }'''


STATUS_DISPLAY_DEVICE_ID = 'ZB:00000004'


def status_display_device(devid=STATUS_DISPLAY_DEVICE_ID,
                          status=const.STATUS_ONLINE,
                          low_battery=False, no_response=False):
    """Status display configurable device mock response."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.bx",
          "type":"Status Display",
          "name":"Status Indicator",
          "area":"1",
          "zone":"11",
          "sort_order":null,
          "is_window":"",
          "bypass":"0",
          "schar_24hr":"0",
          "sresp_mode_0":"5",
          "sresp_entry_0":"5",
          "sresp_exit_0":"5",
          "sresp_mode_1":"5",
          "sresp_entry_1":"5",
          "sresp_exit_1":"5",
          "sresp_mode_2":"5",
          "sresp_entry_2":"5",
          "sresp_exit_2":"5",
          "sresp_mode_3":"5",
          "sresp_entry_3":"5",
          "sresp_exit_3":"5",
          "version":"SSL_00.00.03.03TC",
          "origin":"abode",
          "control_url":"",
          "deep_link":null,
          "status_color":"#5cb85c",
          "faults":{
             "low_battery":''' + str(int(low_battery)) + ''',
             "tempered":0,
             "supervision":0,
             "out_of_order":0,
             "no_response":''' + str(int(no_response)) + '''
          },
          "status":"''' + status + '''",
          "statuses":{
             "hvac_mode":null
          },
          "status_ex":"",
          "actions":[
          ],
          "status_icons":[
          ],
          "siren_default":null,
          "icon":"assets/icons/unknown.svg"
       }'''


IR_CAMERA_DEVICE_ID = 'ZB:00000005'
IR_CAMERA_CONTROL_URL = 'api/v1/cams/ZB:fbb601/capture'


def ir_camera_device(devid=IR_CAMERA_DEVICE_ID, status=const.STATUS_ONLINE,
                     low_battery=False, no_response=False):
    """IR camera configurable device mock response."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.ir_camera",
          "type":"Motion Camera",
          "name":"Downstairs Motion Camera",
          "area":"1",
          "zone":"3",
          "sort_order":null,
          "is_window":"",
          "bypass":"0",
          "schar_24hr":"0",
          "sresp_mode_0":"0",
          "sresp_entry_0":"0",
          "sresp_exit_0":"0",
          "sresp_mode_1":"5",
          "sresp_entry_1":"4",
          "sresp_exit_1":"0",
          "sresp_mode_2":"0",
          "sresp_entry_2":"4",
          "sresp_exit_2":"0",
          "sresp_mode_3":"0",
          "sresp_entry_3":"0",
          "sresp_exit_3":"0",
          "version":"852_00.00.03.05TC",
          "origin":"abode",
          "control_url":"''' + IR_CAMERA_CONTROL_URL + '''",
          "deep_link":null,
          "status_color":"#5cb85c",
          "faults":{
             "low_battery":''' + str(int(low_battery)) + ''',
             "tempered":0,
             "supervision":0,
             "out_of_order":0,
             "no_response":''' + str(int(no_response)) + '''
          },
          "status":"''' + status + '''",
          "statuses":{
             "hvac_mode":null
          },
          "status_ex":"",
          "actions":[
             {
                "label":"Auto Flash",
                "value":"a=1&z=3&req=img;"
             },
             {
                "label":"Never Flash",
                "value":"a=1&z=3&req=img_nf;"
             }
          ],
          "status_icons":[
          ],
          "motion_event":"1",
          "wide_angle":"0",
          "icon":"assets/icons/motioncamera-b.svg"
       }'''


LOCK_DEVICE_ID = 'ZW:0000006'
LOCK_DEVICE_CONTROL_URL = 'api/v1/control/lock/' + LOCK_DEVICE_ID


def lock_device(devid=LOCK_DEVICE_ID, status=const.STATUS_LOCKCLOSED,
                low_battery=False, no_response=False):
    """Lock device configurable device mock response."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.door_lock",
          "type":"Door Lock",
          "name":"Back Door Deadbolt",
          "area":"1",
          "zone":"7",
          "sort_order":"0",
          "is_window":"0",
          "bypass":"0",
          "schar_24hr":"0",
          "sresp_mode_0":"0",
          "sresp_entry_0":"0",
          "sresp_exit_0":"0",
          "sresp_mode_1":"0",
          "sresp_entry_1":"0",
          "sresp_exit_1":"0",
          "sresp_mode_2":"0",
          "sresp_entry_2":"0",
          "sresp_exit_2":"0",
          "sresp_mode_3":"0",
          "sresp_entry_3":"0",
          "sresp_exit_3":"0",
          "version":"",
          "origin":"abode",
          "control_url":"''' + LOCK_DEVICE_CONTROL_URL + '''",
          "deep_link":null,
          "status_color":"#5cb85c",
          "faults":{
             "low_battery":''' + str(int(low_battery)) + ''',
             "tempered":0,
             "supervision":0,
             "out_of_order":0,
             "no_response":''' + str(int(no_response)) + '''
          },
          "status":"''' + status + '''",
          "statuses":{
             "hvac_mode":null
          },
          "status_ex":"",
          "actions":[
             {
                "label":"Lock",
                "value":"a=1&z=7&sw=on;"
             },
             {
                "label":"Unlock",
                "value":"a=1&z=7&sw=off;"
             }
          ],
          "status_icons":{
             "LockOpen":"assets/icons/unlocked-red.svg",
             "LockClosed":"assets/icons/locked-green.svg"
          },
          "automation_settings":null,
          "icon":"assets/icons/automation-lock.svg"
       }'''


POWER_SWITCH_DEVICE_ID = 'ZW:00000007'
POWER_SWITCH_CONTROL_URL = ('api/v1/control/power_switch/'
                            + POWER_SWITCH_DEVICE_ID)


def power_switch_device(devid=POWER_SWITCH_DEVICE_ID, status=const.STATUS_OFF,
                        low_battery=False, no_response=False):
    """Power switch configurable device mock response."""
    return '''
        {
           "id":"''' + devid + '''",
           "type_tag":"device_type.power_switch_sensor",
           "type":"Power Switch Sensor",
           "name":"Back Porch Light",
           "area":"1",
           "zone":"32",
           "sort_order":null,
           "is_window":"",
           "bypass":"0",
           "schar_24hr":"0",
           "sresp_mode_0":"0",
           "sresp_entry_0":"0",
           "sresp_exit_0":"0",
           "sresp_mode_1":"0",
           "sresp_entry_1":"0",
           "sresp_exit_1":"0",
           "sresp_mode_2":"0",
           "sresp_entry_2":"0",
           "sresp_exit_2":"0",
           "sresp_mode_3":"0",
           "sresp_entry_3":"0",
           "sresp_exit_3":"0",
           "capture_mode":null,
           "origin":"abode",
           "control_url":"''' + POWER_SWITCH_CONTROL_URL + '''",
           "deep_link":null,
           "status_color":"#5cb85c",
           "faults":{
              "low_battery":''' + str(int(low_battery)) + ''',
              "tempered":0,
              "supervision":0,
              "out_of_order":0,
              "no_response":''' + str(int(no_response)) + '''
           },
           "status":"''' + status + '''",
           "statuses":{
              "hvac_mode":null
           },
           "status_ex":"",
           "actions":[
              {
                 "label":"Switch off",
                 "value":"a=1&z=32&sw=off;"
              },
              {
                 "label":"Switch on",
                 "value":"a=1&z=32&sw=on;"
              },
              {
                 "label":"Toggle",
                 "value":"a=1&z=32&sw=toggle;"
              },
              {
                 "label":"Switch on for 5 min",
                 "value":"a=1&z=32&sw=on&pd=5;"
              },
              {
                 "label":"Switch on for 10 min",
                 "value":"a=1&z=32&sw=on&pd=10;"
              },
              {
                 "label":"Switch on for 15 min",
                 "value":"a=1&z=32&sw=on&pd=15;"
              },
              {
                 "label":"Switch on for 20 min",
                 "value":"a=1&z=32&sw=on&pd=20;"
              },
              {
                 "label":"Switch on for 25 min",
                 "value":"a=1&z=32&sw=on&pd=25;"
              },
              {
                 "label":"Switch on for 30 min",
                 "value":"a=1&z=32&sw=on&pd=30;"
              },
              {
                 "label":"Switch on for 45 min",
                 "value":"a=1&z=32&sw=on&pd=45;"
              },
              {
                 "label":"Switch on for 1 hour",
                 "value":"a=1&z=32&sw=on&pd=60;"
              },
              {
                 "label":"Switch on for 2 hours",
                 "value":"a=1&z=32&sw=on&pd=120;"
              },
              {
                 "label":"Switch on for 5 hours",
                 "value":"a=1&z=32&sw=on&pd=300;"
              },
              {
                 "label":"Switch on for 8 hours",
                 "value":"a=1&z=32&sw=on&pd=480;"
              }
           ],
           "status_icons":[
           ],
           "icon":"assets/icons/plug.svg"
        }'''


WATER_SENSOR_DEVICE_ID = 'RF:00000008'


def water_sensor_device(devid=WATER_SENSOR_DEVICE_ID,
                        status=const.STATUS_OFF,
                        low_battery=False, no_response=False):
    """Water sensor configurable device mock response."""
    return '''
        {
           "id":"''' + devid + '''",
           "type_tag":"device_type.water_sensor",
           "type":"Water Sensor",
           "name":"Downstairs Bathroo",
           "area":"1",
           "zone":"26",
           "sort_order":"0",
           "is_window":"0",
           "bypass":"0",
           "schar_24hr":"1",
           "sresp_mode_0":"0",
           "sresp_entry_0":"0",
           "sresp_exit_0":"0",
           "sresp_mode_1":"0",
           "sresp_entry_1":"0",
           "sresp_exit_1":"0",
           "sresp_mode_2":"0",
           "sresp_entry_2":"0",
           "sresp_exit_2":"0",
           "sresp_mode_3":"0",
           "sresp_entry_3":"0",
           "sresp_exit_3":"0",
           "capture_mode":null,
           "origin":"abode",
           "control_url":"",
           "deep_link":null,
           "status_color":"#5cb85c",
           "faults":{
              "low_battery":''' + str(int(low_battery)) + ''',
              "tempered":0,
              "supervision":0,
              "out_of_order":0,
              "no_response":''' + str(int(no_response)) + '''
           },
           "status":"''' + status + '''",
           "statuses":{
              "hvac_mode":null
           },
           "status_ex":"",
           "actions":[
           ],
           "status_icons":[
           ],
           "icon":"assets/icons/water-value-shutoff.svg"
        }'''


SECURE_BARRIER_DEVICE_ID = 'ZW:0000000a'
SECURE_BARRIER_CONTROL_URL = ('api/v1/control/power_switch/'
                              + SECURE_BARRIER_DEVICE_ID)


def secure_barrier_device(devid=SECURE_BARRIER_DEVICE_ID,
                          status=const.STATUS_OPEN,
                          low_battery=False, no_response=False):
    """Secure barrier configurable device mock response."""
    return '''
        {
           "id":"''' + devid + '''",
           "type_tag":"device_type.secure_barrier",
           "type":"Secure Barrier",
           "name":"Garage Auto Door",
           "area":"1",
           "zone":"11",
           "sort_order":"0",
           "is_window":"0",
           "bypass":"0",
           "schar_24hr":"0",
           "sresp_mode_0":"0",
           "sresp_entry_0":"0",
           "sresp_exit_0":"0",
           "sresp_mode_1":"0",
           "sresp_entry_1":"0",
           "sresp_exit_1":"0",
           "sresp_mode_2":"0",
           "sresp_entry_2":"0",
           "sresp_exit_2":"0",
           "sresp_mode_3":"0",
           "sresp_entry_3":"0",
           "sresp_exit_3":"0",
           "capture_mode":null,
           "origin":"abode",
           "control_url":"api/v1/control/power_switch/ZW:00000006",
           "deep_link":null,
           "status_color":"#5cb85c",
           "faults":{
              "low_battery":''' + str(int(low_battery)) + ''',
              "tempered":0,
              "supervision":0,
              "out_of_order":0,
              "no_response":''' + str(int(no_response)) + '''
           },
           "status":"''' + status + '''",
           "statuses":{
              "hvac_mode":null
           },
           "status_ex":"",
           "actions":[
              {
                 "label":"Close",
                 "value":"a=1&z=11&sw=off;"
              },
              {
                 "label":"Open",
                 "value":"a=1&z=11&sw=on;"
              }
           ],
           "status_icons":{
              "Open":"assets/icons/garage-door-red.svg",
              "Closed":"assets/icons/garage-door-green.svg"
           },
           "icon":"assets/icons/garage-door.svg"
        }'''
