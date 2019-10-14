"""Mock Abode Power Switch Sensor Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZW:00000105'
CONTROL_URL = 'api/v1/control/light/' + DEVICE_ID


def device(devid=DEVICE_ID, status=CONST.STATUS_OFF,
           level=0, low_battery=False, no_response=False):
    """Dimmer  mock device."""
    return '''
      {
         "id":"''' + devid + '''",
         "type_tag":"device_type.dimmer",
         "type":"Dimmer",
         "name":"Kitchen Lights",
         "area":"1",
         "zone":"12",
         "sort_order":"",
         "is_window":"",
         "bypass":"0",
         "schar_24hr":"0",
         "sresp_24hr":"0",
         "sresp_mode_0":"0",
         "sresp_entry_0":"0",
         "sresp_exit_0":"0",
         "group_name":"Ungrouped",
         "group_id":"1",
         "default_group_id":"1",
         "sort_id":"10000",
         "sresp_mode_1":"0",
         "sresp_entry_1":"0",
         "sresp_exit_1":"0",
         "sresp_mode_2":"0",
         "sresp_entry_2":"0",
         "sresp_exit_2":"0",
         "sresp_mode_3":"0",
         "uuid":"fcc65fb7d52cdf7b080a2005539e30a4",
         "sresp_entry_3":"0",
         "sresp_exit_3":"0",
         "sresp_mode_4":"0",
         "sresp_entry_4":"0",
         "sresp_exit_4":"0",
         "version":"",
         "origin":"abode",
         "has_subscription":null,
         "onboard":"0",
         "s2_grnt_keys":"",
         "s2_dsk":"",
         "s2_propty":"",
         "s2_keys_valid":"",
         "zwave_secure_protocol":"",
         "control_url":"''' + CONTROL_URL + '''",
         "deep_link":null,
         "status_color":"#5cb85c",
         "faults":{
            "low_battery":''' + str(int(low_battery)) + ''',
            "tempered":0,
            "supervision":0,
            "out_of_order":0,
            "no_response":''' + str(int(no_response)) + ''',
            "jammed":0,
            "zwave_fault":0
         },
         "status":"''' + status + '''",
         "status_display":"OFF",
         "statuses":{
            "saturation":"N/A",
            "hue":"N/A",
            "level":"''' + str(int(level)) + '''",
            "switch":"0",
            "color_temp":"N/A",
            "color_mode":"N/A"
         },
         "status_ex":"",
         "actions":[
            {
               "label":"Switch off",
               "value":"a=1&z=12&sw=off;"
            },
            {
               "label":"Switch on",
               "value":"a=1&z=12&sw=on;"
            },
            {
               "label":"Toggle",
               "value":"a=1&z=12&sw=toggle;"
            },
            {
               "label":"0%",
               "value":"a=1&z=12&sw=0;"
            },
            {
               "label":"10%",
               "value":"a=1&z=12&sw=10;"
            },
            {
               "label":"20%",
               "value":"a=1&z=12&sw=20;"
            },
            {
               "label":"30%",
               "value":"a=1&z=12&sw=30;"
            },
            {
               "label":"40%",
               "value":"a=1&z=12&sw=40;"
            },
            {
               "label":"50%",
               "value":"a=1&z=12&sw=50;"
            },
            {
               "label":"60%",
               "value":"a=1&z=12&sw=60;"
            },
            {
               "label":"70%",
               "value":"a=1&z=12&sw=70;"
            },
            {
               "label":"80%",
               "value":"a=1&z=12&sw=80;"
            },
            {
               "label":"90%",
               "value":"a=1&z=12&sw=90;"
            },
            {
               "label":"100%",
               "value":"a=1&z=12&sw=99;"
            }
         ],
         "status_icons":[

         ],
         "statusEx":"0",
         "icon":"assets/icons/bulb-1.svg"
      }'''
