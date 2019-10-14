"""Mock Abode Power Switch Sensor Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZB:00000106'
DEVICE_UUID = 'abcd33455232fff31232'
CONTROL_URL = 'api/v1/control/light/' + DEVICE_ID
INTEGRATIONS_URL = CONST.INTEGRATIONS_URL + DEVICE_UUID


def color_temp_post_response_ok(devid, color_temp):
    """Return color temp change response json."""
    return '''
      {
         "idForPanel": "''' + devid + '''",
         "colorTemperature": ''' + str(int(color_temp)) + '''
      }'''


def color_post_response_ok(devid, hue, saturation):
    """Return color change response json."""
    return '''
      {
         "idForPanel": "''' + devid + '''",
         "hue": ''' + str(int(hue)) + ''',
         "saturation": ''' + str(int(saturation)) + '''
      }'''


def device(devid=DEVICE_ID, uuid=DEVICE_UUID, status=CONST.STATUS_OFF,
           level=0, saturation=57, hue=60, color_temp=6536,
           color_mode=CONST.COLOR_MODE_OFF, low_battery=False,
           no_response=False):
    """Hue  mock device."""
    return '''
      {
         "id":"''' + devid + '''",
         "type_tag":"device_type.hue",
         "type":"RGB Dimmer",
         "name":"Overhead Light",
         "area":"1",
         "zone":"30",
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
         "uuid":"''' + DEVICE_UUID + '''",
         "sresp_entry_3":"0",
         "sresp_exit_3":"0",
         "sresp_mode_4":"0",
         "sresp_entry_4":"0",
         "sresp_exit_4":"0",
         "version":"LST002",
         "origin":"abode",
         "has_subscription":null,
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
         "statuses":{
            "saturation":''' + str(int(saturation)) + ''',
            "hue":''' + str(int(hue)) + ''',
            "level":"''' + str(int(level)) + '''",
            "switch":"1",
            "color_temp":''' + str(int(color_temp)) + ''',
            "color_mode":"''' + str(int(color_mode)) + '''"
         },
         "status_ex":"",
         "actions":[
            {
               "label":"Switch off",
               "value":"a=1&z=30&sw=off;"
            },
            {
               "label":"Switch on",
               "value":"a=1&z=30&sw=on;"
            },
            {
               "label":"Toggle",
               "value":"a=1&z=30&sw=toggle;"
            },
            {
               "label":"0%",
               "value":"a=1&z=30&sw=0;"
            },
            {
               "label":"10%",
               "value":"a=1&z=30&sw=10;"
            },
            {
               "label":"20%",
               "value":"a=1&z=30&sw=20;"
            },
            {
               "label":"30%",
               "value":"a=1&z=30&sw=30;"
            },
            {
               "label":"40%",
               "value":"a=1&z=30&sw=40;"
            },
            {
               "label":"50%",
               "value":"a=1&z=30&sw=50;"
            },
            {
               "label":"60%",
               "value":"a=1&z=30&sw=60;"
            },
            {
               "label":"70%",
               "value":"a=1&z=30&sw=70;"
            },
            {
               "label":"80%",
               "value":"a=1&z=30&sw=80;"
            },
            {
               "label":"90%",
               "value":"a=1&z=30&sw=90;"
            },
            {
               "label":"100%",
               "value":"a=1&z=30&sw=99;"
            }
         ],
         "status_icons":[
         ],
         "statusEx":"37",
         "icon":"assets/icons/bulb-1.svg"
      }'''
