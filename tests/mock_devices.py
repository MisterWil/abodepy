"""
Mock devices that mimic actual device data from Abode servers.
This file should be updated any time the Abode server responses
change so we can make sure abodepy can still communicate.
"""

import helpers.constants as const

GLASS_BREAK_DEVICE_ID = 'RF:00000001'
def GLASS_BREAK_DEVICE(id=GLASS_BREAK_DEVICE_ID, status=const.STATUS_ONLINE, low_battery=False, no_response=False):
    return '\
        {  \
          "id":"'+id+'",\
          "type_tag":"device_type.glass",\
          "type":"GLASS",\
          "name":"Glass Break Sensor",\
          "area":"1",\
          "zone":"6",\
          "sort_order":null,\
          "is_window":"",\
          "bypass":"0",\
          "schar_24hr":"0",\
          "sresp_mode_0":"0",\
          "sresp_entry_0":"0",\
          "sresp_exit_0":"0",\
          "sresp_mode_1":"5",\
          "sresp_entry_1":"5",\
          "sresp_exit_1":"0",\
          "sresp_mode_2":"5",\
          "sresp_entry_2":"5",\
          "sresp_exit_2":"0",\
          "sresp_mode_3":"5",\
          "sresp_entry_3":"5",\
          "sresp_exit_3":"0",\
          "version":"",\
          "origin":"abode",\
          "control_url":"",\
          "deep_link":null,\
          "status_color":"#5cb85c",\
          "faults":{  \
             "low_battery":'+str(int(low_battery))+',\
             "tempered":0,\
             "supervision":0,\
             "out_of_order":0,\
             "no_response":'+str(int(no_response))+'\
          },\
          "status":"'+status+'",\
          "statuses":{  \
             "hvac_mode":null\
          },\
          "status_ex":"",\
          "actions":[  \
          ],\
          "status_icons":[  \
          ],\
          "icon":"assets\/icons\/unknown.svg"\
       }'

KEYPAD_DEVICE_ID = 'RF:00000002'
def KEYPAD_DEVICE(id=KEYPAD_DEVICE_ID, status=const.STATUS_ONLINE, low_battery=False, no_response=False):
    return '\
       {  \
          "id":"'+id+'",\
          "type_tag":"device_type.keypad",\
          "type":"Keypad",\
          "name":"Keypad",\
          "area":"1",\
          "zone":"10",\
          "sort_order":null,\
          "is_window":"",\
          "bypass":"0",\
          "schar_24hr":"0",\
          "sresp_mode_0":"5",\
          "sresp_entry_0":"5",\
          "sresp_exit_0":"5",\
          "sresp_mode_1":"5",\
          "sresp_entry_1":"5",\
          "sresp_exit_1":"5",\
          "sresp_mode_2":"5",\
          "sresp_entry_2":"5",\
          "sresp_exit_2":"5",\
          "sresp_mode_3":"5",\
          "sresp_entry_3":"5",\
          "sresp_exit_3":"5",\
          "version":"",\
          "origin":"abode",\
          "control_url":"",\
          "deep_link":null,\
          "status_color":"#5cb85c",\
          "faults":{  \
             "low_battery":'+str(int(low_battery))+',\
             "tempered":0,\
             "supervision":0,\
             "out_of_order":0,\
             "no_response":'+str(int(no_response))+'\
          },\
          "status":"'+status+'",\
          "statuses":{  \
             "hvac_mode":null\
          },\
          "status_ex":"",\
          "actions":[  \
          ],\
          "status_icons":[  \
          ],\
          "icon":"assets\/icons\/keypad-b.svg"\
       }'
   
DOOR_CONTACT_DEVICE_ID = 'RF:00000003'
def DOOR_CONTACT_DEVICE(id=DOOR_CONTACT_DEVICE_ID, status=const.STATUS_CLOSED, low_battery=False, no_response=False):
    return '\
        {  \
          "id":"'+id+'",\
          "type_tag":"device_type.door_contact",\
          "type":"Door Contact",\
          "name":"Back Door",\
          "area":"1",\
          "zone":"2",\
          "sort_order":null,\
          "is_window":"",\
          "bypass":"0",\
          "schar_24hr":"0",\
          "sresp_mode_0":"3",\
          "sresp_entry_0":"3",\
          "sresp_exit_0":"0",\
          "sresp_mode_1":"1",\
          "sresp_entry_1":"1",\
          "sresp_exit_1":"0",\
          "sresp_mode_2":"1",\
          "sresp_entry_2":"1",\
          "sresp_exit_2":"0",\
          "sresp_mode_3":"1",\
          "sresp_entry_3":"1",\
          "sresp_exit_3":"0",\
          "version":"",\
          "origin":"abode",\
          "control_url":"",\
          "deep_link":null,\
          "status_color":"#5cb85c",\
          "faults":{  \
             "low_battery":'+str(int(low_battery))+',\
             "tempered":0,\
             "supervision":0,\
             "out_of_order":0,\
             "no_response":'+str(int(no_response))+'\
          },\
          "status":"'+status+'",\
          "statuses":{  \
             "hvac_mode":null\
          },\
          "status_ex":"",\
          "actions":[  \
          ],\
          "status_icons":{  \
             "Open":"assets\/icons\/door-open-red.svg",\
             "Closed":"assets\/icons\/door-closed-green.svg"\
          },\
          "sresp_trigger":"0",\
          "sresp_restore":"0",\
          "icon":"assets\/icons\/doorsensor-a.svg"\
       }'
       
STATUS_DISPLAY_DEVICE_ID = 'ZB:00000004'
def STATUS_DISPLAY_DEVICE(id=STATUS_DISPLAY_DEVICE_ID, status=const.STATUS_ONLINE, low_battery=False, no_response=False):
    return '\
        {  \
          "id":"'+id+'",\
          "type_tag":"device_type.bx",\
          "type":"Status Display",\
          "name":"Status Indicator",\
          "area":"1",\
          "zone":"11",\
          "sort_order":null,\
          "is_window":"",\
          "bypass":"0",\
          "schar_24hr":"0",\
          "sresp_mode_0":"5",\
          "sresp_entry_0":"5",\
          "sresp_exit_0":"5",\
          "sresp_mode_1":"5",\
          "sresp_entry_1":"5",\
          "sresp_exit_1":"5",\
          "sresp_mode_2":"5",\
          "sresp_entry_2":"5",\
          "sresp_exit_2":"5",\
          "sresp_mode_3":"5",\
          "sresp_entry_3":"5",\
          "sresp_exit_3":"5",\
          "version":"SSL_00.00.03.03TC",\
          "origin":"abode",\
          "control_url":"",\
          "deep_link":null,\
          "status_color":"#5cb85c",\
          "faults":{  \
             "low_battery":'+str(int(low_battery))+',\
             "tempered":0,\
             "supervision":0,\
             "out_of_order":0,\
             "no_response":'+str(int(no_response))+'\
          },\
          "status":"'+status+'",\
          "statuses":{  \
             "hvac_mode":null\
          },\
          "status_ex":"",\
          "actions":[  \
          ],\
          "status_icons":[  \
          ],\
          "siren_default":null,\
          "icon":"assets\/icons\/unknown.svg"\
       }'
       
IR_CAMERA_DEVICE_ID = 'ZB:00000005'
def IR_CAMERA_DEVICE(id=IR_CAMERA_DEVICE_ID, status=const.STATUS_ONLINE, low_battery=False, no_response=False):
    return '\
        {  \
          "id":"'+id+'",\
          "type_tag":"device_type.ir_camera",\
          "type":"Motion Camera",\
          "name":"Downstairs Motion Camera",\
          "area":"1",\
          "zone":"3",\
          "sort_order":null,\
          "is_window":"",\
          "bypass":"0",\
          "schar_24hr":"0",\
          "sresp_mode_0":"0",\
          "sresp_entry_0":"0",\
          "sresp_exit_0":"0",\
          "sresp_mode_1":"5",\
          "sresp_entry_1":"4",\
          "sresp_exit_1":"0",\
          "sresp_mode_2":"0",\
          "sresp_entry_2":"4",\
          "sresp_exit_2":"0",\
          "sresp_mode_3":"0",\
          "sresp_entry_3":"0",\
          "sresp_exit_3":"0",\
          "version":"852_00.00.03.05TC",\
          "origin":"abode",\
          "control_url":"api\/v1\/cams\/ZB:fbb601\/capture",\
          "deep_link":null,\
          "status_color":"#5cb85c",\
          "faults":{  \
             "low_battery":'+str(int(low_battery))+',\
             "tempered":0,\
             "supervision":0,\
             "out_of_order":0,\
             "no_response":'+str(int(no_response))+'\
          },\
          "status":"'+status+'",\
          "statuses":{  \
             "hvac_mode":null\
          },\
          "status_ex":"",\
          "actions":[  \
             {  \
                "label":"Auto Flash",\
                "value":"a=1&z=3&req=img;"\
             },\
             {  \
                "label":"Never Flash",\
                "value":"a=1&z=3&req=img_nf;"\
             }\
          ],\
          "status_icons":[  \
          ],\
          "motion_event":"1",\
          "wide_angle":"0",\
          "icon":"assets\/icons\/motioncamera-b.svg"\
       }'
       
LOCK_DEVICE_ID = 'ZW:0000006'
def LOCK_DEVICE(id=LOCK_DEVICE_ID, status=const.STATUS_LOCKCLOSED, low_battery=False, no_response=False):
    return '\
        {  \
          "id":"'+id+'",\
          "type_tag":"device_type.door_lock",\
          "type":"Door Lock",\
          "name":"Back Door Deadbolt",\
          "area":"1",\
          "zone":"7",\
          "sort_order":"0",\
          "is_window":"0",\
          "bypass":"0",\
          "schar_24hr":"0",\
          "sresp_mode_0":"0",\
          "sresp_entry_0":"0",\
          "sresp_exit_0":"0",\
          "sresp_mode_1":"0",\
          "sresp_entry_1":"0",\
          "sresp_exit_1":"0",\
          "sresp_mode_2":"0",\
          "sresp_entry_2":"0",\
          "sresp_exit_2":"0",\
          "sresp_mode_3":"0",\
          "sresp_entry_3":"0",\
          "sresp_exit_3":"0",\
          "version":"",\
          "origin":"abode",\
          "control_url":"api\/v1\/control\/lock\/ZW:00000002",\
          "deep_link":null,\
          "status_color":"#5cb85c",\
          "faults":{  \
             "low_battery":'+str(int(low_battery))+',\
             "tempered":0,\
             "supervision":0,\
             "out_of_order":0,\
             "no_response":'+str(int(no_response))+'\
          },\
          "status":"'+status+'",\
          "statuses":{  \
             "hvac_mode":null\
          },\
          "status_ex":"",\
          "actions":[  \
             {  \
                "label":"Lock",\
                "value":"a=1&z=7&sw=on;"\
             },\
             {  \
                "label":"Unlock",\
                "value":"a=1&z=7&sw=off;"\
             }\
          ],\
          "status_icons":{  \
             "LockOpen":"assets\/icons\/unlocked-red.svg",\
             "LockClosed":"assets\/icons\/locked-green.svg"\
          },\
          "automation_settings":null,\
          "icon":"assets\/icons\/automation-lock.svg"\
       }'